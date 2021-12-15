#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan

def callback(data):
    for i in range(420,660):
        pub = rospy.Publisher('isObstacle', Bool, queue_size=10)
        rate = rospy.Rate(200) # 10hz
        if (data.ranges[i]<0.2):
            pub.publish(True)
            rospy.loginfo(rospy.get_caller_id() + 'I heard %f %i',data.ranges[i],i)


def obstacle():


    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('obstacle', anonymous=True)


    rospy.Subscriber('base_scan', LaserScan, callback)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    obstacle()
