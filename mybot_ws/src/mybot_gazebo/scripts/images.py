#!/usr/bin/env python
import rospy
#from my_subscriber.msg import Person
import rospkg 
from gazebo_msgs.msg import ModelState 
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
from time import sleep
from time import time as tm
import string
# from tool.darknet2pytorch import Darknet
# from demo import *

# board=Darknet('cfg/yolov4_box.cfg',inference=True)
# board.load_weights('backup/yolov4_box_4000.weights')
# board.cuda()

# module=Darknet('cfg/yolov4_module.cfg',inference=True)
# module.load_weights('backup/yolov4_module_4000.weights')
# module.cuda()

# def my_detect(m,cv_img):
#   use_cuda=True
#   img=cv2.resize(cv_img, (m.width, m.height))
#   img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#   boxes = do_detect(m, img, 0.4, 0.6, use_cuda)
#   if len(boxes[0])==0:
#     return [False,0,0,0,0]
#   box=boxes[0][0]
#   h,w,c=cv_img.shape
#   x1 = int(box[0] * w)
#   y1 = int(box[1] * h)
#   x2 = int(box[2] * w)
#   y2 = int(box[3] * h)
#   return [True,x1,y1,x2,y2]
  
# def end_to_end(board,module,cv_img):
#   use_cuda=True
#   img=cv2.resize(cv_img, (board.width, board.height))
#   img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#   boxes = do_detect(board, img, 0.4, 0.6, use_cuda)
#   if len(boxes[0])==0:
#     return [False,0,0,0,0]
#   box=boxes[0][0]
#   h,w,c=cv_img.shape
#   x1 = int(box[0] * w)
#   y1 = int(box[1] * h)
#   x2 = int(box[2] * w)
#   y2 = int(box[3] * h)
  
#   hc=y2-y1
#   wc=x2-x1

#   x1=max(0,x1)
#   x2=min(board.width,x2)
#   y1=max(0,y1)
#   y2=min(board.height,y2)
#   if (x2-x1)*(y2-y1)==0 :
#     return [False,0,0,0,0]
#   cropped=cv2.resize(cv_img[y1:y2,x1:x2], (module.width,module.height))
#   # imShow(cropped)
#   cropped=cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
#   boxes=do_detect(module, cropped, 0.4, 0.6, use_cuda)
#   if len(boxes[0])==0:
#     return [False,0,0,0,0]
#   box=boxes[0][0]
#   # print(box,hc,wc,x1,y1)
#   a1=x1+int(box[0]*wc)
#   b1=y1+int(box[1]*hc)
#   a2=x1+int(box[2]*wc)
#   b2=y1+int(box[3]*hc)
#   # print(a1,b1,a2,b2)
#   return [True,a1,b1,a2,b2]
t0=tm()
# writer=cv2.VideoWriter('video18.avi',  
#                          cv2.VideoWriter_fourcc(*'MJPG'), 
#                          30, (512,512)) 

ind=0
command='circle1'
char=0
for c in string.ascii_lowercase :
    filenames=glob.glob('train/img{}*.jpg'.format(char))
    if len(filenames)==0 :
        char=c
        break

def callback(data):
    # global board
    # global module
    global ind
    global command
    global t0
    t=tm()
    dt=0.5*(t-t0)
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

    amp=2
    R=amp*np.sin(dt)
    r=np.pi/6*np.sin(np.sqrt(7)/2*dt)
    p=0
    y=0

    # if command=='circle1' :
    #     x=amp*np.sin(0.3*dt)
    #     Y=-amp*np.cos(0.3*dt)
    #     z=0
    #     r=0
    #     # p=0.6
    #     y=np.pi/2-0.3*dt

    # if command=='circle1' and 0.3*dt>np.pi :
    #     command='circle2'
    #     t0=tm()
    #     dt=0

    # if command=='circle2':
    #     x=amp*np.sin(0.3*dt)
    #     Y=amp*np.cos(0.3*dt)
    #     z=0
    #     r=0
    #     # p=0.6
    #     y=-np.pi/2+0.3*dt

    # if command=='circle2' and 0.3*dt>np.pi/2 :
    #     t0=tm()
    #     dt=0
    #     command='straight'

    # if command=='straight':
    #     x=amp-0.5*dt
    #     Y=0#-amp*np.cos(0.3*dt)
    #     z=0
    #     r=0
    #     # p=0.6
    #     y=0#np.pi/2-0.3*dt
    #     if x<0.05 :
    #         writer.release()
    #         print('done')


    cr=np.cos(r/2)
    cp=np.cos(p/2)
    cy=np.cos(y/2)
    sr=np.sin(r/2)
    sp=np.sin(p/2)
    sy=np.sin(y/2)
    
    # cv_image=cv2.resize(cv_image,(320,320))
    # x=(amp-R)
    # y=-0.25+(amp-R)/2*np.cos(np.e/2*dt)
    # z=(amp-R)/4*np.sin(np.sqrt(5)*dt)
    
    ct=np.cos(0.9)
    st=np.sin(0.9)
    state_msg = ModelState()
    state_msg.model_name = 'mybot'
    state_msg.pose.position.x = 10-amp+R#4.1-x*ct+z*st#4.3-amp+R
    state_msg.pose.position.y = (amp-R)/2*np.cos(np.e/2*dt)#-0.25+Y#-0.05+(amp-R)/2*np.cos(np.e/2*dt)
    state_msg.pose.position.z = 1.51+(amp-R)/4*np.sin(np.sqrt(5)*dt)#1.51+x*st+z*ct#1.2+(amp-R)/4*np.sin(np.sqrt(5)*dt)
    state_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
    state_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
    state_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
    state_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy

    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    pub.publish(state_msg)
    # ret,x1,y1,x2,y2=my_detect(board,cv_image)
    # ret,x1,y1,x2,y2=my_detect(module,cv_image)
    # ret,x1,y1,x2,y2=end_to_end(board,module,cv_image)

    # cv_image=cv2.rectangle(cv_image,(x1,y1),(x2,y2),(0,0,255),2)
    img=cv2.resize(cv_image,(512,512))
    cv2.imwrite('train/img{}{:03d}.jpg'.format(char,ind),img)
    # writer.write(img)
    ind+=1
    cv2.imshow('frame',img)
    cv2.waitKey(50)
    # if ind>=900:
    # 	writer.release()
    # 	print('done')
    
    
def listener():
	rospy.init_node('ml',anonymous=True)
	#global velocity_pub
	# global ind 
	# rospy.init_node('main')
	image_sub = rospy.Subscriber("/mybot/camera1/image_raw",Image,callback)
	rospy.spin()
  

if __name__ == '__main__':
    listener()