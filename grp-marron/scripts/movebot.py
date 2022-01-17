#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from random import *

pub= False
rotating=False

def move():
    global pub

    rospy.init_node('move', anonymous=True)
    pub = rospy.Publisher(
        '/cmd_vel_mux/input/navi',
        Twist, queue_size=10
    )
    rospy.Subscriber('isObstacle', String, move_command)
    rospy.spin()

def rotation(data):
    global rotating
    rotating=False

# Publish velocity commandes:
def move_command(data):
    global rotating


    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    if rotating==False:
        time=uniform(0.6,1.6)
        if data.data=="D":
            cmd.angular.z=1
            rotating=True
            rospy.Timer(rospy.Duration(time),rotation,oneshot=True)
            
        elif data.data=="G":
            cmd.angular.z=-1
            rotating=True
            rospy.Timer(rospy.Duration(time),rotation,oneshot=True)
            
        
        else:
            cmd.linear.x= 0.5
        
        pub.publish(cmd)

if __name__ == '__main__':
    move()

