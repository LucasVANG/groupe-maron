#!/usr/bin/python3

import rospy,math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


rospy.init_node('obstacle', anonymous=True)
pub = rospy.Publisher('isObstacle', String, queue_size=5)


def interpret_scan(data):
    global pub
    obstacles= []
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment

    rospy.loginfo( 'I get scans:' + str(len(obstacles)) + ' over ' + str(len(data.ranges)) )
    for t in obstacles:
        if(0.1 < t[0] < 0.5):
            if( -0.25 < t[1] < 0):
                pub.publish("D")
                rospy.loginfo(t)

            if( 0.25 > t[1] > 0 ):
                pub.publish("G")
                rospy.loginfo(t)
        else:
            pub.publish("r")


rospy.Subscriber('scan', LaserScan, interpret_scan)
rospy.spin()

