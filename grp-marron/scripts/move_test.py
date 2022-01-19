#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray


pub= False
vitesse=0
def move():
    global pub
    rospy.init_node('detection', anonymous=True)
    pub = rospy.Publisher(
        '/cmd_vel_mux/input/navi',
        Twist, queue_size=10
    )
    rospy.Subscriber('isObstacle', Int32MultiArray, move_command)
    rospy.spin()

def move_command(data):
    global pub
    cmd=Twist()
    vitesse_lin=data.data[0]
    vitesse_ang=data.data[1]

    #On définit la vitesse linéaire, vitesse_lin peut avoir c'est valeur 0 1 2 3 4 5 qui correspondent à des vitesses respectivement de 0 2 3 4 5 6 (afin de pouvoir modifié facilement chaque cas)
    if vitesse_lin==0:

        cmd.linear.x=0
    elif vitesse_lin==1:

        cmd.linear.x=0.2
    elif vitesse_lin==2:

        cmd.linear.x=0.3
    elif vitesse_lin==3:

        cmd.linear.x=0.5
    elif vitesse_lin==4:

        cmd.linear.x=0.25
    elif vitesse_lin==5:

        cmd.linear.x=0
    
    cmd.linear.x=adapt_speed(cmd.linear.x)
    #On déninit la vitesse angulaire  vitesse_ang peut avoir c'est valeur 0 1 2 3 4 5 6 qui correspondent à des vitesses respectivement de 1 -0.5 -0.2 0.2 0.5 0 0.1
    if vitesse_ang==0:
        
        cmd.angular.z=1
    elif vitesse_ang==1:

        cmd.angular.z=-0.5
    elif vitesse_ang==2:
    
        cmd.angular.z=-0.2
    elif vitesse_ang==3:
    
        cmd.angular.z=0.2
    elif vitesse_ang==4:
    
        cmd.angular.z=0.5
    elif vitesse_ang==5:
    
        cmd.angular.z=0
    elif vitesse_ang==6:
    
        cmd.angular.z=0.1
    
    pub.publish(cmd)

def adapt_speed(data): #Pour incrémenter lentement la vitesse
    global vitesse 
    if(vitesse>data.linear.x):
        vitesse+=0.1
    elif(vitesse<data.linear.x):
        vitesse-=0.1
    return vitesse
    



    


if __name__ == '__main__':
    move()