#!/usr/bin/env python
"""
This script applies sense pre-trained models to Gesture Control for SmartTVs.

List of controls:
  - Play/Pause: Raise hand
  - Next channel: Swipe left
  - Previous channel: Swipe right
  - Automatic pause when the user leaves

Usage:
  run_smart_tv_demo.py [--camera_id=CAMERA_ID]
                       [--path_in=FILENAME]
                       [--path_out=FILENAME]
                       [--title=TITLE]
                       [--use_gpu]
  run_smart_tv_demo.py (-h | --help)

Options:
  --custom_classifier=PATH   Path to the custom classifier to use
  --path_in=FILENAME         Video file to stream from
  --path_out=FILENAME        Video file to stream to
  --title=TITLE              This adds a title to the window display
"""
from docopt import docopt

import sense.display
from sense.loading import load_weights_from_resources
from sense.controller import Controller
from sense.downstream_tasks.nn_utils import LogisticRegression
from sense.downstream_tasks.nn_utils import Pipe
from sense.downstream_tasks.postprocess import PostprocessClassificationOutput
from sense.loading import build_backbone_network
from sense.loading import update_backbone_weights
from sense.loading import ModelConfig


LAB2INT = {
    "background": 0,
    "hold-raised-hand": 1,
    "ignore_1": 2,
    "ignore_2": 3,
    "ignore_3": 4,
    "person-has-left": 5,
    "person-still-there": 6,
    "raising-hand": 7,
    "sitting-down": 8,
    "sitting-down-end": 9,
    "standing-up": 10,
    "swiping-left": 11,
    "swiping-left-end": 12,
    "swiping-right": 13,
    "swiping-right-end": 14,
    "walking": 15,
    "walking-to-sofa-and-sit": 16
}
INT2LAB = {value: key for key, value in LAB2INT.items()}


if __name__ == "__main__":
    # Parse arguments
    args = docopt(__doc__)
    camera_id = int(args['--camera_id'] or 0)
    path_in = args['--path_in'] or None
    path_out = args['--path_out'] or None
    title = args['--title'] or None
    use_gpu = args['--use_gpu']

    # Load backbone network according to config file
    backbone_model_config = ModelConfig('StridedInflatedEfficientNet', 'pro', [])
    backbone_weights = backbone_model_config.load_weights()['backbone']

    # Load custom classifier
    checkpoint_classifier = load_weights_from_resources('smarttv_gesture_control/sien_pro_last_9_layers_float16.ckpt')

    # Update original weights in case some intermediate layers have been finetuned
    update_backbone_weights(backbone_weights, checkpoint_classifier)

    # Create backbone network
    backbone_network = build_backbone_network(backbone_model_config, backbone_weights)

    gesture_classifier = LogisticRegression(num_in=backbone_network.feature_dim,
                                            num_out=len(INT2LAB))
    gesture_classifier.load_state_dict(checkpoint_classifier)
    gesture_classifier.eval()

    # Concatenate feature extractor and met converter
    net = Pipe(backbone_network, gesture_classifier)

    postprocessor = [
        PostprocessClassificationOutput(INT2LAB, smoothing=1)
    ]

    display_ops = [
        sense.display.DisplayFPS(expected_camera_fps=net.fps,
                                 expected_inference_fps=net.fps / net.step_size),
        sense.display.DisplayTopKClassificationOutputs(top_k=1, threshold=0.1),
        sense.display.SmartTVButtons()
    ]
    display_results = sense.display.DisplayResults(title=title, display_ops=display_ops)

    # Run live inference
    controller = Controller(
        neural_network=net,
        post_processors=postprocessor,
        results_display=display_results,
        callbacks=[],
        camera_id=camera_id,
        path_in=path_in,
        path_out=path_out,
        use_gpu=use_gpu
    )
    controller.run_inference()
