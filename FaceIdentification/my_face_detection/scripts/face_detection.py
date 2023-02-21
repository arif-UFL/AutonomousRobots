#!/usr/bin/env python3
import cv2
import rospy
import numpy as np
# improt bridge to convert images to rospy frames
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

def callback(inp_image):
    try:
        imag = bridge.imgmsg_to_cv2(inp_image, "bgr8")
    except CvBridgeError as e:
        print(e)
    if imag is None:
        print('frame dropped, skipping')
    else:
        # ImageProcessor(imag)
        # trained xml file to detect the face recognition
        faceCascade = cv2.CascadeClassifier('/home/arif/catkin_ws/src/my_face_detection/scripts/haarcascade_frontalface_default.xml')
        # GrayScale conversion
        gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
        blurFrame = cv2.GaussianBlur(gray,(25,25),0)

        #Face Detection scanning
        faces = faceCascade.detectMultiScale(blurFrame,1.5,5)

        # Draw a rectangle around the faces
        for (x,y,w,h) in faces:
            #draw rectangles
            cv2.rectangle(imag, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+h]
            roi_color= imag[y:y+h, x:x+h]
        # Coversion of cv2 image to ROS Message    
        ros_imag = bridge.cv2_to_imgmsg(imag, encoding="bgr8")
    # Publish the final Result
    Pub.publish(ros_imag)

        
if __name__ == '__main__':
    #Creating a ROS Node
    rospy.init_node('Face_detection_node', anonymous=True)
    # OpenCV bridge instance creation
    bridge = CvBridge()
    # ROS Subscriber for topic /usb_cam/image_raw ( Input from USB Camera)
    Sub = rospy.Subscriber('/usb_cam/image_raw', Image, callback, queue_size=5)
    # Publishing the OutPut Image after processing
    Pub = rospy.Publisher('/out/image', Image, queue_size=5)
    rospy.spin()