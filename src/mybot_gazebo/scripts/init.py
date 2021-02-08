#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
from time import sleep
from time import time as tm 

from light import find_nav_lights

depth=0#np.random.rand([800,800])
def callback_depth(data):
	global depth
	bridge = CvBridge()
	cv_img = bridge.imgmsg_to_cv2(data,"passthrough")
	depth=np.array(cv_img,dtype=np.float32)
	# cv2.imshow('depth',depth)
	# cv2.waitKey(50)

def callback_color(data):
	bridge = CvBridge()
	cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
	rs,rc,gs,gc=find_nav_lights(cv_img)
	print(rs,rc,gs,gc,depth[rc[1]][rc[0]],depth[gc[1]][gc[0]])
	cv2.imshow('color',cv_img)
	cv2.waitKey(50)

def main():
	# global velocity_pub
	# global ind 
	rospy.init_node('init')
	# velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#sub_laser_front = rospy.Subscriber('/hexbot/laser/scan', LaserScan , callback_frontlaser)
	depth_sub = rospy.Subscriber("/camera/depth/image_raw",Image,callback_depth)
	image_sub = rospy.Subscriber("/camera/color/image_raw",Image,callback_color)
	#image_sub2 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, pickup)
	#image_sub3 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, see_tag_and_put)
	rospy.spin()

if __name__ == '__main__':
	main() 