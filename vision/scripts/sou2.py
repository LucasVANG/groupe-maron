#!/usr/bin/python3
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int32MultiArray
rospy.init_node('objet', anonymous=True)
pub = rospy.Publisher(
    'can',   
    Int32MultiArray, queue_size=10
)

color=10

lo=np.array([color-5, 100, 50])
hi=np.array([color+5, 255,100])

color_info=(0, 0, 255)

cap=cv2.VideoCapture(-1)
cv2.namedWindow('Camera')
cmd=Int32MultiArray()

while True:
    ret, frame=cap.read()
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=1)
    mask=cv2.dilate(mask, None, iterations=1)
    image2=cv2.bitwise_and(frame, frame, mask= mask)
    
    # Affichage des composantes HSV sous la souris sur l'image
    image=cv2.blur(image, (7, 7))
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
               

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        ((x, y), rayon)=cv2.minEnclosingCircle(c)
        if rayon>30:
            cmd.data=[int(x),int(y)]
            pub.publish(cmd)
            cv2.circle(image2, (int(x), int(y)), int(rayon), color_info, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
            
    cv2.imshow('Camera', frame)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()