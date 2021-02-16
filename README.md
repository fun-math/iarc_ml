# iarc_ml

## Updates

- Added *detect.py*. This is an example of a ROS node subscribing to the camera topic and running the model on it.
- Trained module on new mast\
Update the cfg file to *yolov4_module_new.cfg* and the weights file too to run the new model.
- Trained module with yolov4 tiny which runs at 64fps on colab (as opposed to 20fps for yolov4).\
Update the cfg file to *yolov4-tiny_module.cfg* and the weights file too to run the tiny model.\
Note : There was a bug in *darknet2pytorch.py*. So clone again to run tiny model. 
- Added package *full_mast* which has mast with the text. Copy *full_mast* directory to *.gazebo/models* 
- Defined a function *find_nav_lights* in *light.py* \
`[red_state,red_centre,green_state,green_centre]=find_nav_lights(cv_img)` \
*state* is a string which takes values "On", "Off" or "Not Found" \
*centre* is tuple of integers (x,y)
- Trained board with yolov4 tiny too and this runs at 60fps in colab but **didn't give good accuracy** \
Update the cfg file to *yolov4-tiny_box.cfg* and the weights file too to run the tiny model.\
- Trained board with new model \
The same config file works but change the weights to that in *board_new* link 
- Trained board with both the old and new data \
Performs better than just the new data \
The same config file works but change the weights to that in *board_both* link.

## Weights

Download the weights from these drive links and keep it in the *backup* folder.

- [board](https://drive.google.com/file/d/1W63HaBdtmTq_cT1u0SDh5tvrRmQTD4zI/view?usp=sharing)
- [module](https://drive.google.com/file/d/1-aGdPU61z8n1VrkYkSnyJPlVrKuZUq4A/view?usp=sharing)
- [module_new](https://drive.google.com/file/d/1Mbv-Mt756YZ_OKRp_Sf20Q3lilPeooei/view?usp=sharing)\
- [tiny_module](https://drive.google.com/file/d/1VfXnKt03awvFPVqv9OVbZf6G2q3r_pEB/view?usp=sharing)
- [tiny_board](https://drive.google.com/file/d/1-SEM0MKr6sb2d08MtECCvZcRvIefOnwU/view?usp=sharing)
- [board_new](https://drive.google.com/file/d/17jcKUu4u31MrMppSytGsX5uE-gKAEwEL/view?usp=sharing)
- [board_both](https://drive.google.com/file/d/1-5dOSINKSGN2sZnJMQD-285nPFEHiEj-/view?usp=sharing)\
\
Finally, here are the best weights that we propose. For each task, there is a yolov4 model and a yolov4-tiny. Yolov4 models would run at \~30fps. The tiny models would be slightly inaccurate but would be 3 times fast. Let's test both and pick the one that suits our needs :D \
Further much of the unnecessary confusion with cfg files is now reduced. If you need to use any yolov4 model then keep *yolov4.cfg* as config file and if you want to use any tiny model then keep *yolov4-tiny.cfg* as config file.\

- [board](https://drive.google.com/file/d/1-5dOSINKSGN2sZnJMQD-285nPFEHiEj-/view?usp=sharing)
- [module](https://drive.google.com/file/d/1-2MB7MFfRD5oe43yE6jEGEjhKyF6SpcD/view?usp=sharing)
- [tiny_board](https://drive.google.com/file/d/1-ekzkABBt4WBWUQxPTWqa-a5P8MjO4Vn/view?usp=sharing)
- [tiny_module](https://drive.google.com/file/d/11NEg8h_StiHcexYYNIBUrZIeWjNuXe-L/view?usp=sharing)


## Usage 

A class *Darknet* is defined and both the pytorch models are instances of this class.

`model=Darknet('cfg/cfg_file.cfg',inference=True)`\
`model.load_weights('backup/weights_file.weights')`\
`model.cuda()`

Two functions *my_detect* and *end_to_end* are defined in *iarc.py*.

`ret,x1,y1,x2,y2=my_detect(model,cv_img)`

Expects the cv_img in BGR format with entries in [0,255] and the pytorch model.\
Returns a list of boolean flag (true if bbox predicted) and four integers (x1,y1) is the coordinate of top left corner and (x2,y2) is the coordinate of the bottom right corner. Returns 0's if no box is detected. (Note : x axis is the width of image)

`ret,x1,y1,x2,y2=end_to_end(board,module,cv_img)`

Expects the cv_img in BGR format with entries in [0,255] and both pytorch models.\
Directly returns coorinates of bounding box of module from raw image. Format is similar as above.

## Pictures

- `ret,x1,y1,x2,y2=my_detect(board,cv_img)`

![board model](pytorch-yolov4/data/board.jpg)

- `ret,x1,y1,x2,y2=my_detect(module,cv_img)`

![module model](pytorch-yolov4/data/module.jpg)

- `ret,x1,y1,x2,y2=end_to_end(board,module,cv_img)`

![both models using *end_to_end*](pytorch-yolov4/data/end_to_end.jpg)

## References 

- darknet-[https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)
- pytorch-[https://github.com/Tianxiaomo/pytorch-YOLOv4](https://github.com/Tianxiaomo/pytorch-YOLOv4)