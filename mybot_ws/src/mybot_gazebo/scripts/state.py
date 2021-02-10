#!/usr/bin/env python
import rospy
#from my_subscriber.msg import Person
import rospkg 
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.srv import SetModelState

#from std_msgs.msg import String
#from nav_msgs.msg import Odometry

set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

i=0

def callback():
    global i 
    #rospy.loginfo( "I heard %f", data.pose.pose.position.x)         #The %f or %d or whatever 
                                                                        #determines the number of places after decimal      
    state_msg = ModelState()
    state_msg.model_name = 'full_mast'
    state_msg.pose.position.x = i
    state_msg.pose.position.y = 0
    state_msg.pose.position.z = 0
    state_msg.pose.orientation.x = 0
    state_msg.pose.orientation.y = 0
    state_msg.pose.orientation.z = 0
    state_msg.pose.orientation.w = 0

    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    rate = rospy.Rate(100)
    pub.publish(state_msg)                           #This part publishes what it heard 
                                                #from the mavros/local_position/odom to gazebo

    i+=1e-2

def listener():

    rospy.init_node('my_node',anonymous=True)
    callback()
    #rospy.Subscriber('/mavros/local_position/odom',Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()