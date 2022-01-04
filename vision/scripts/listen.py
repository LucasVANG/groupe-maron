#!/usr/bin/python3
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int32MultiArray

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %i %i',data.data[0],data.data[1])

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('can', Int32MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
