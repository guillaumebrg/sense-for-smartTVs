Note: Please note that this repo is a fork of `sense`: https://github.com/TwentyBN/sense.
Models showcased here are finetuned using the pre-trained weights and training tools available in the original repo.

## Gesture control for SmartTVs 

This repo demoes an RGB-based gesture control system for smart TVs. The following controls are supported:
  - Play/Pause: Raise hand
  - Next channel: Swipe left
  - Previous channel: Swipe right
  - Automatic pause when the user leaves

<div align="center">

<p align="center">
    <img src="https://raw.githubusercontent.com/guillaumebrg/sense-for-smartTVs/master/resources/smarttv_gesture_control/video_test.gif" width="600px">
</p>

</div>

Try it yourself: 

```shell
PYTHONPATH=./ python examples/run_smart_tv_demo.py --use_gpu
```


#### Installation steps & Troubleshooting

Please refer to the original repo for requirements & installation steps: https://github.com/TwentyBN/sense

Once everything is installed, you can check that the model is working fine by running it on the test video
provided in the resources folder:

```shell
PYTHONPATH=./ python examples/run_smart_tv_demo.py --path_in=resources/smarttv_gesture_control/video_test.mp4
```

Model predictions should be similar to what is shown in the GIF above. In case you see a difference, check 
the model framerate, displayed at the bottom-left corner; it should be close to 4 FPS. A framerate lower 
than 4 indicates that your CPU isn't able to perform inference fast enough. If you have one, you may want 
to run the model on the GPU instead, appending `--use_gpu` to the above-mentioned command line.


## License 

The code is MIT but pretrained weights come with a separate license available. Please check the original 
[sense repo](https://github.com/TwentyBN/sense) for more information.