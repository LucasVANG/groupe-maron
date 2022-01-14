#!/usr/bin/env python3

import rospy
import numpy as np

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker
from std_msgs.msg import String
import math as mth
import tf
from std_srvs.srv import SetBool

rospy.init_node("new_bottle")
pub = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

def print_Bottle(req):
    global list_bottle
    msg=''
    if not any(t[2]>10 for t in list_bottle):
        return (False,"Aucune bouteille presente")
    else:
        for a in range(len(list_bottle)):
            if list_bottle[a][2]>10:
                msg+="[x=" + str(list_bottle[a][0])+","+"y="+ str(list_bottle[a][1])+"]"
    return (True, "Voici les coordonnees des bouteilles detectees: " + msg)


tfListener = tf.TransformListener()
rospy.Service('Liste_Bouteille', SetBool,print_Bottle)
list_bottle=[]
i=0

def initialize_marker(i,x,y):
    marker = Marker()
    marker.header.frame_id = 'map' #self.global_frame
    marker.header.stamp=rospy.Time.now()
    marker.ns= "marker"
    marker.id= i
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z=0.1
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.5
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 0.08
    marker.scale.y = 0.08
    marker.scale.z = 0.16
    return marker

def marker(data):
    global pub,i,list_bottle
    global tfListener
    poseMap= tfListener.transformPose("map", data)
    x=poseMap.pose.position.x
    y=poseMap.pose.position.y
    bouteille=initialize_marker(i,x,y)
 

    if not list_bottle:
        list_bottle=[[x,y,1]]
        i+=1
    else:
        
        if all(( mth.sqrt((x-n[0])**2 + (y-n[1])**2))>0.3 for n in list_bottle):
            list_bottle.append([x,y,1])
            i+=1
        else:
            for a in range(0,i,1):
                print(a,list_bottle[a])
                if (( mth.sqrt((x-list_bottle[a][0])**2 + (y-list_bottle[a][1])**2))<0.2):
                    list_bottle[a][0]=(list_bottle[a][0]+x)/2
                    list_bottle[a][1]=(list_bottle[a][1]+y)/2
                    list_bottle[a][2]+=1
                    if (list_bottle[a][2])>10:
                        pub.publish(initialize_marker(a,list_bottle[a][0],list_bottle[a][1]))
                for b in range(0,a,1):
                    dist = mth.sqrt((list_bottle[b][0]-list_bottle[a][0])**2 + (list_bottle[b][1]-list_bottle[a][1])**2)
                    if dist<0.1:
                        bottle=initialize_marker(a,list_bottle[a][0],list_bottle[a][1])
                        bottle.action=Marker.DELETE
                        list_bottle.pop(a)
                        i-=1
                        pub.publish(bottle)
                        print(len(list_bottle))
                        

                        



    
def start():
    rospy.Subscriber('/can',PoseStamped, marker)
    rospy.spin()
if __name__ == '__main__':
    start()

