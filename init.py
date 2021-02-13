#! /usr/bin/env python

import rospy
import rospkg 
from gazebo_msgs.msg import ModelState
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

ind=0
depth=0#np.random.rand([800,800])
t0=tm()
def callback_depth(data):
	global depth
	bridge = CvBridge()
	cv_img = bridge.imgmsg_to_cv2(data,"passthrough")
	depth=np.array(cv_img,dtype=np.float32)
	# cv2.imshow('depth',depth)
	# cv2.waitKey(50)

theta=2*np.pi*np.random.rand()
X=5-5*np.cos(theta)
Y=-5*np.sin(theta)
y=theta
command='init'
quad=0
# rospy.init_node('init')
pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
# r0=0
# p0=0
# y0=0
# cr=np.cos(r0/2)
# cp=np.cos(p0/2)
# cy=np.cos(y0/2)
# sr=np.sin(r0/2)
# sp=np.sin(p0/2)
# sy=np.sin(y0/2)
# state_msg = ModelState()
# state_msg.model_name = 'hunter_killer_mast'
# state_msg.pose.position.x = 10
# state_msg.pose.position.y = 0
# state_msg.pose.position.z = 0
# state_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
# state_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
# state_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
# state_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy
# pub.publish(state_msg)
def callback_color(data):
	global t0
	global X
	global Y
	global command 
	global quad
	global y
	global pub
	global ind 
	dt=tm()-t0
	bridge = CvBridge()
	cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
	rs,rc,gs,gc=find_nav_lights(cv_img)
	
	print(rs,(rc[0],rc[1]),gs,(gc[0],gc[1]),depth[rc[1]][rc[0]],depth[gc[1]][gc[0]])
	
	dr=depth[rc[1]][rc[0]]
	dg=depth[gc[1]][gc[0]]

	dr=-1 if (np.isnan(dr) or rs=='Not Found') else dr
	dg=-1 if (np.isnan(dg) or rs=='Not Found') else dg
	done=False
	
	if command=='init' :
		r0=0
		p0=0
		y0=-1.57

		R0=3*np.random.rand()
		theta0=2*np.pi*np.random.rand()

		cr=np.cos(r0/2)
		cp=np.cos(p0/2)
		cy=np.cos(y0/2)
		sr=np.sin(r0/2)
		sp=np.sin(p0/2)
		sy=np.sin(y0/2)

		state_msg = ModelState()
		state_msg.model_name = 'hunter_killer_mast'
		state_msg.pose.position.x = 5+R0*np.cos(theta0)
		state_msg.pose.position.y = R0*np.sin(theta0)
		state_msg.pose.position.z = 0.05
		state_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
		state_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
		state_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
		state_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy
		pub.publish(state_msg)

		r=0
		p=0
		y=np.arctan2(-Y,5-X)

		cr=np.cos(r/2)
		cp=np.cos(p/2)
		cy=np.cos(y/2)
		sr=np.sin(r/2)
		sp=np.sin(p/2)
		sy=np.sin(y/2)

		state_msg = ModelState()
		state_msg.model_name = 'mybot'
		state_msg.pose.position.x = X
		state_msg.pose.position.y = Y
		state_msg.pose.position.z = 2
		state_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
		state_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
		state_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
		state_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy
		pub.publish(state_msg)
		command='start'

	if ind<5 :
		ind+=1
		return

	if command=='start':
		# if dr==-1 and dg==-1 :
		# 	continue

		if dr!=-1 and dg!=-1:
			if rc[0]<gc[0] :
				if dr<dg :
					quad=4
				else :
					quad=1
			else :
				if dr<dg :
					quad=3
				else :
					quad=2

		elif dr!=-1:
			quad=4

		elif dg!=-1:
			quad=1

	if quad==1 or quad==2 :
		if dr==-1 or dg==-1 or dr>dg :
			command='left'
		else :
			print('done')
			done=True

	if quad==4 or quad==3:
		if dr==-1 or dg==-1 or dr<dg :
			command='right'
		else :
			print('done')
			done=True



	# if rs=='Not Found' :
	# 	rc[0]=1e6

	# if gs=="Not Found":
	# 	gc[0]=-1e6
	# if np.isnan(dr) :
	# 	dr=100

	# if np.isnan(dg) :
	# 	dg=200



	# if rc[0]>gc[0] or abs(dr-dg)>0.05 :
	# 	temp=X
	# 	# X=X+0.5*Y
	# 	# Y=Y-0.5*(5-temp)
	# else :
	# 	print('done')
	# 	done=True
	r=0
	p=0
	# y=0

	if command=='left' :
		temp=X
		X=X+0.01*Y
		Y=Y+0.01*(5-temp)
		# y=y-0.01*np.sqrt(5)

	if command=='right':
		temp=X
		X=X-0.01*Y
		Y=Y-0.01*(5-temp)
		# y=y+0.01*np.sqrt(5)

	y=np.arctan2(-Y,5-X)

	cr=np.cos(r/2)
	cp=np.cos(p/2)
	cy=np.cos(y/2)
	sr=np.sin(r/2)
	sp=np.sin(p/2)
	sy=np.sin(y/2)

	state_msg = ModelState()
	state_msg.model_name = 'mybot'
	state_msg.pose.position.x = X
	state_msg.pose.position.y = Y
	state_msg.pose.position.z = 2
	state_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
	state_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
	state_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
	state_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy


	if not done :
		pub.publish(state_msg)
	cv2.imshow('color',cv_img)
	cv2.waitKey(50)

def main():
	# global velocity_pub
	# global ind 
	global pub
	rospy.init_node('init')
	# velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#sub_laser_front = rospy.Subscriber('/hexbot/laser/scan', LaserScan , callback_frontlaser)
	# pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
	depth_sub = rospy.Subscriber("/camera/depth/image_raw",Image,callback_depth)
	image_sub = rospy.Subscriber("/camera/color/image_raw",Image,callback_color)
	#image_sub2 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, pickup)
	#image_sub3 = rospy.Subscriber("/hexbot/camera1/image_raw",Image, see_tag_and_put)
	rospy.spin()

if __name__ == '__main__':
	main() 