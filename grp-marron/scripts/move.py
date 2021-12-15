#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool


def move():
    rospy.init_node('move', anonymous=True)
    global pub
    pub = rospy.Publisher(
        '/cmd_vel',
        Twist, queue_size=10
    )
    rospy.Subscriber('isObstacle', Bool, move_command)
    rospy.spin()

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    if data.data==True:
        cmd= Twist()
        cmd.angular.z=0.3
        pub.publish(cmd)
    if data.data==False:
        cmd= Twist()
        cmd.linear.x= 0.1
        pub.publish(cmd)

    
if __name__ == '__main__':
    move()
# call the move_command at a regular frequency:
