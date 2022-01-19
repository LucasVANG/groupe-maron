#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray


pub= False
vitesse=0
tourne=0
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
    speed=data.data[0]
    spin=data.data[1]
    speed=speed/100
    spin=spin/100
    cmd.linear.x=adapt_speed(speed)
    cmd.angular.z=adapt_tourne(spin)
    pub.publish(cmd)

def adapt_speed(data): #Pour incrémenter lentement la vitesse
    global vitesse 
    if(vitesse<data):
        vitesse+=0.04
    elif(vitesse>data):
        vitesse-=0.04
    return vitesse

def adapt_tourne(data):
    global tourne
    if(tourne<data):
        tourne+=0.05
    elif(tourne>data):
        tourne-=0.05
    return tourne
    



    


if __name__ == '__main__':
    move()
