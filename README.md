Note: Please note that this repo is a fork built on top of the main `sense` repository: https://github.com/TwentyBN/sense.
Models showcased here were finetuned using the pre-trained weights and training tools available in the original repo.

## Gesture control for SmartTVs 

This repo demoes a gesture control system for smart TVs. The following controls were implemented:
  - Play/Pause: Raise hand
  - Next channel: Swipe left
  - Previous channel: Swipe right
  - Automatic pause when the user leaves

<div align="center">

<p align="center">
    <img src="https://raw.githubusercontent.com/guillaumebrg/sense-for-smartTVs/fix-readme/resources/smarttv_gesture_control/video_test.gif" width="600px">
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
than 4 indicates that your CPU isn't able to perform inference fast enough. To fix it, you may want to
use your GPU instead, appending `--use_gpu` to the above-mentioned command line.


#### Training details

TODO

---

## License 

The code is MIT but retrained weights come with a separate license available. Please check the original 
[sense repo](https://github.com/TwentyBN/sense) for more information.