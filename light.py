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

# ind=0
def find_nav_lights(cv_img):

	img=cv_img.copy()
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	b,g,r=np.rollaxis(img,2,0)
	h,s,v=np.rollaxis(img_hsv,2,0)

	mask_gray=((r-g)^2+(g-b)^2+(b-r)^2)>200
	mask_gray=mask_gray*(200<s)
	mask_green = (h<65)*(55<h)*mask_gray 
	#print(mask.shape)
	mask_red = (h<5)+(175<h)
	mask_red=mask_red*mask_gray

	res_green=img_gray*mask_green
	res_red=img_gray*mask_red

	res_green=cv2.GaussianBlur(res_green,(5,5),0)
	res_red=cv2.GaussianBlur(res_red,(5,5),0)

	_,thresh = cv2.threshold(res_red,0,255,cv2.THRESH_BINARY)
	_, contours, hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)
	red_state='Not Found'
	red_centre=(0,0)
	for  cnt in contours :
		# if cv2.contourArea(cnt)<200:
			# continue
		mask=np.zeros_like(res_red)
		mask=cv2.drawContours(mask,[cnt],0,255,-1)
		mask=mask/255.0
		#print(np.sum(img_gray*mask),np.sum(mask))
		M=cv2.moments(cnt)
		red_centre=(M['m10']/M['m00'],M['m01']/M['m00'])
			
		if np.sum(img_gray*mask)/np.sum(mask)>40 :
			red_state='On'
			img=cv2.drawContours(img,[cnt],0,(0,255,0),3)
		else :
			red_state='Off'
			img=cv2.drawContours(img,[cnt],0,(255,255,255),3)


	_,thresh = cv2.threshold(res_green,0,255,cv2.THRESH_BINARY)
	_, contours, hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,
	cv2.CHAIN_APPROX_SIMPLE)
	green_state='Not Found'
	green_centre=(0,0)
	for  cnt in contours :
		# if cv2.contourArea(cnt)<200:
			# continue
		mask=np.zeros_like(res_red)
		mask=cv2.drawContours(mask,[cnt],0,255,-1)
		mask=mask/255.0
		M=cv2.moments(cnt)
		green_centre=(M['m10']/M['m00'],M['m01']/M['m00'])
			
		if np.sum(img_gray*mask)/np.sum(mask)>40 :
			green_state="On"	
			img=cv2.drawContours(img,[cnt],0,(0,0,255),3)
		else :
			green_state="Off"
			img=cv2.drawContours(img,[cnt],0,(128,128,0),3)

	# print(cv_img[rc[1]][rc[0]],cv_img[gc[1]][gc[0]])
	cv2.imshow('img_new',img)
	cv2.waitKey(50)
	return [red_state,np.rint(np.array(red_centre)).astype(np.int32),green_state,np.rint(np.array(green_centre)).astype(np.int32)]
	#res_green=cv2.GaussianBlur(res_green,(5,5),0)
	#res=cv2.inRange(img_hsv,(30,0,0),(90,255,255))
	
	# cv2.imshow('img',cv_img)
	#cv2.imshow('res_green',res_green)
	#cv2.imshow('res_red',res_red)
		

def callback_opencv(data):
	bridge = CvBridge()
	cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
	
	rs,rc,gs,gc=find_nav_lights(cv_img)
	print(cv_img[rc[1]][rc[0]],cv_img[gc[1]][gc[0]])
	# print(rs,rc,gs,gc)

def main():
	global velocity_pub
	global ind 
	rospy.init_node('main')
	velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#sub_laser_front = rospy.Subscriber('/hexbot/laser/scan', LaserScan , callback_frontlaser)
	image_sub = rospy.Subscriber("/camera/color/image_raw",Image,callback_opencv)
	#image_sub2 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, pickup)
	#image_sub3 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, see_tag_and_put)
	rospy.spin()

if __name__ == '__main__':
	main()