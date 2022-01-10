#!/usr/bin/python3
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
 

def interpret_image(data):
    temp_frame=data
    global bridge,color,lo,hi,color_info
    frame = bridge.imgmsg_to_cv2(temp_frame, desired_encoding='passthrough')
    
    cv2.namedWindow('Camera')
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Camera',frame )
    cv2.waitKey(40)
    cmd=Int32MultiArray()

    image=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=1)
    mask=cv2.dilate(mask, None, iterations=1)
    image2=cv2.bitwise_and(frame, frame, mask= mask)
        
        # Affichage des composantes HSV sous la souris sur l'image
    image=cv2.blur(image, (7, 7))
    mask=cv2.erode(mask, None, iterations=1)
    mask=cv2.dilate(mask, None, iterations=1)
                

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        ((x, y), rayon)=cv2.minEnclosingCircle(c)
        if rayon<400:
            cmd.data=[int(x),int(y)]
            pub.publish(cmd)
            cv2.circle(image2, (int(x), int(y)), int(rayon), color_info, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
                
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
 
cv2.destroyAllWindows()

def testback(data):
    rospy.loginfo("hello")

def detection():
    global lo,hi,pub,color_info
    rospy.init_node('objet', anonymous=True)
    pub = rospy.Publisher(
        'can',   
        Int32MultiArray, queue_size=10
    )
    rospy.loginfo(rospy.get_caller_id() + 'I heard ')
    color=175

    lo=np.array([100, 125, 125])
    hi=np.array([120, 175,175])

    color_info=(0, 0, 255)
    rospy.Subscriber('camera/color/image_raw', Image, interpret_image)
    rospy.spin()

if __name__ == '__main__':
    detection()