#!/usr/bin/env python3

import rospy
import numpy as np
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import Marker
from std_msgs.msg import String
import math as mths

rospy.init_node("new_bottle")
pub = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)
list_bottle=[]
x=0
y=0
i=0

def initialize_marker():
    print("test")
    global x,y
    marker = Marker()
    marker.header.frame_id = 'map' #self.global_frame
    marker.header.stamp=rospy.Time.now()
    marker.ns= "marker"
    marker.id= x
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z= 1.5
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 1
    marker.scale.y = 1
    marker.scale.z = 3
    return marker

def marker(data):
    bouteille=initialize_marker()
    global pub,x,y,i,list_bottle

    

    if not list_bottle:
        list_bottle=[[1,1], [4,4],[8,7],[16,18]]
    else:
        
        if all(( mth.sqrt((x-n[0])**2 + (y-n[1])**2))>5 for n in list_bottle):
            list_bottle.append([x,y])
            print(list_bottle)
        
            pub.publish(bouteille)

    print(list_bottle)
    x+=1
    y=x
    
def start():
    rospy.Subscriber('chatter', String, marker)
    rospy.spin()
if __name__ == '__main__':
    start()

