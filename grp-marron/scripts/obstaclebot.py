#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32MultiArray

# Initiglobal alize ROS::node
rospy.init_node('detection', anonymous=True)

pub = rospy.Publisher(
    '/isObstacle',
    Int32MultiArray, queue_size=10
)

def obs_plus_proches(data):
    angle= data.angle_min
    angle_min_G=0
    angle_min_D=0
    dist_min_G=100
    dist_min_D=100
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 and angle > -1.5 and angle < 1.5:
            if angle < 0:
                if dist_min_G > aDistance:
                    dist_min_G=aDistance
                    angle_min_G=angle
            else:
                if dist_min_D > aDistance:
                    dist_min_D=aDistance
                    angle_min_D=angle
            
        angle+= data.angle_increment
    return dist_min_G,angle_min_G,dist_min_D,angle_min_D

def ecart(angle_G, angle_D, dis_G, dis_D): 
    
    pointA= [math.cos(angle_G) * dis_G, math.sin( angle_G ) * dis_G]
    pointB= [math.cos(angle_D) * dis_D, math.sin( angle_D ) * dis_D]
    euclidis= math.sqrt((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)
    if (euclidis<0.4):
        tourne=100
        vitesse=3
        print("STOP")
    else:
        tourne=0
        vitesse=25
    return vitesse , tourne



def interpret_scan(data):
    global pub
    msg = Int32MultiArray()
    dis_gau,angle_gau,dis_dro,angle_dro=obs_plus_proches(data) 

    if dis_gau < dis_dro:
        dis=dis_gau
        angle=angle_gau
    else:
        dis= dis_dro
        angle=angle_dro

    vit_lin=30
    vit_angular=0

    if dis < 0.6: 
        if dis < 0.30 :
             vit_lin=4
        elif dis < 0.45 :
             vit_lin= 20
        elif dis >= 0.45 :
             vit_lin= 30

        if angle > 0:
            vit_angular = -20
            if dis< 0.5: 
                vit_angular= -50
        elif angle < 0:
            vit_angular = 20
            if dis < 0.5:
                vit_angular=50
        else:
            vit_angular=0

    
        if dis_dro > dis_gau-0.05 and dis_dro < dis_gau+0.05 and dis < 0.5:
            speed,spin=ecart(angle_gau,angle_dro,dis_gau,dis_dro)

    else: 
        vit_angular = 0
        vit_lin = 40
    msg.data.append(int( vit_lin))
    msg.data.append(int(vit_angular))
    pub.publish(msg)



rospy.Subscriber("/scan", LaserScan, interpret_scan )
# spin() enter the program in a infinite loopx²
rospy.spin()
