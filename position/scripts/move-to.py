#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
import tf


def callback(data):
    global tfListener
    print(data)
    local_goal= tfListener.transformPose("/odom", data)
    print(local_goal)
def move():
    rospy.init_node('objet', anonymous=True)
    global tfListener
    tfListener = tf.TransformListener()
    rospy.Subscriber('move_base_simple/goal', PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    move()