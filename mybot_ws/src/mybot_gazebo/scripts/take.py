#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
from time import sleep 

f=-2
# t0=rospy.Time.now.to_sec()
ind=0
def callback_opencv(data):
	global ind 
	# v=Twist()
	# t=rospy.Time.now.to_sec()

	# v.linear.x=0.25*np.cos(t-t0)
	# v.linear.y=0.25*np.sin(t-t0)
	#v.angular.z=0.01
	# velocity_pub.publish(v)
	bridge = CvBridge()
	cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	# if ind<10:
	# 	#cv2.imwrite('img{}.jpg'.format(ind),cv_image)
	# 	ind+=1
	# 	print(ind)
	if ind<1:
		cv2.imwrite('img{}.jpg'.format(f),cv_image)
	ind+=1
	print('done')


def main():
	global velocity_pub
	global ind 
	rospy.init_node('main')
	velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#sub_laser_front = rospy.Subscriber('/hexbot/laser/scan', LaserScan , callback_frontlaser)
	image_sub = rospy.Subscriber("/mybot/camera1/image_raw",Image,callback_opencv)
	#image_sub2 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, pickup)
	#image_sub3 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, see_tag_and_put)
	
	if ind < 2:
		rospy.spin()

if __name__ == '__main__':
	main()
