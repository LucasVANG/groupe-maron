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
    time=uniform(1,2)
    print(rotating)
    if data.data=="R":
        cmd.linear.x=0.5
    elif data.data=="S":
        cmd.angular.z=1
    elif data.data=="V":
        cmd.linear.x=0.2
    elif data.data=="TV":
        cmd.linear.x=0.3

if __name__ == '__main__':
    move()

