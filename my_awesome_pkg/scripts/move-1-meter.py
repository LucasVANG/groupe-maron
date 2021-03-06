#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard ')





# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    rospy.Subscriber('scan', LaserScan, callback)
    cmd.linear.x= 0.1
    commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()
