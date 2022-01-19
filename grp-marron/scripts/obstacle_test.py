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
    angle_start=data.angle_min
    angle_G = angle_D = 0
    dis_G = dis_D = 1000
    for d in data.ranges:
        if 0.1<d and d>5.0 and angle_start>(-math.pi)/2 and angle_start<math.pi/2:
            if angle_start>0:
                if dis_D>d:
                    dis_D=d
                    angle_D=angle_start
            else:
                if dis_G>d:
                    dis_G=d
                    angle_G=angle_start
        angle_start+=data.angle_increment
    return dis_G,angle_G,dis_D,angle_D

def etroit(data,dis_D,dis_G,angle_D,angle_G):
    
    point_G=[ math.cos(angle_G) * dis_G , math.sin(angle_G) * dis_G ]#On passe les deux points d'intérets en coordonnées cartésiennes
    point_D=[ math.cos(angle_D) * dis_D , math.sin(angle_D) * dis_D ]
    ecart=math.sqrt((point_G[0] - point_D[0] )**2 + (point_G[1] - point_D[1] )**2)
    #On calcule si la distance entre les deux obstacles à les dimensions du robot
    if ecart<0.25:
        msg.data[0]=6
        msg.data[1]=1
    else:
        msg.data[0]=25
        msg.data[1]=0
    return msg



def interpret_scan(data):
    global pub
    msg = Int32MultiArray()
    dis_G,angle_G,dis_D,angle_D=obs_plus_proches(data) #On recupére les deux obstacles les plus proches à gauche et à droite

    # On détermine lequel est le plus dangereux des deux
 # liste valeurs pour [0] 0 2 3 5 25 6   ==> 0 1 2 3 4 5 
 # liste valeurs pour [1] 10 -5 -2 2 5 0 1  ==> 0 1 2 3 4 5 6
    if dis_G>dis_D:
        dis=dis_D
        angle=angle_D
    else:
        dis=dis_G
        angle=angle_G
    
    

    if dis<0.6:
        if dis<0.4:
            msg.data[0]=0
            msg.data[1]=10
        elif dis<0.5:
            msg.data[0]=1
        elif dis>=0.5:
            msg.data[0]=3
        
        if angle>0:
            msg.data[1]=-2
            if dis<0.5:
                msg.data[1]=-5
        elif angle<0:
            msg.data[1]=2
            if dis<0.5:
                msg.data[1]=5
        else:
            msg.data[1]=0

        if (dis_D+0.05)>dis_G and (dis_D-0.05)<dis_G and dis <0.5:
            msg=etroit(data,dis_D,dis_G,angle_D,angle_G)
    else:
        msg=[5,0]
    pub.publish(msg)



rospy.Subscriber("/scan", LaserScan, interpret_scan )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()