#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

pub= False

def move():
    global pub

    rospy.init_node('move', anonymous=True)
    pub = rospy.Publisher(
        '/cmd_vel',
        Twist, queue_size=10
    )
    rospy.Subscriber('isObstacle', String, move_command)
    rospy.spin()

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()

    if data.data=="D":
        cmd.angular.z=0.2
    elif data.data=="G":
        cmd.angular.z=-0.2
    else:
        cmd.linear.x= 0.2
    
    pub.publish(cmd)

if __name__ == '__main__':
    move()

