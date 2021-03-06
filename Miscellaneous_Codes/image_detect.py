#!/usr/bin/env python2

import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import	Image
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int32
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class WayPoint:
	
	def __init__(self):

		rospy.init_node('ros_bridge')
		self.image_pub = rospy.Publisher('/usb_cam/image_rect_color',Image)
		# Create a ROS Bridge
		self.ros_bridge = cv_bridge.CvBridge()

		# Subscribe to whycon image_out
		self.image_sub = rospy.Subscriber('/whycon/image_out', Image, self.image_callback, queue_size =1)
		# self.image_sub = rospy.Subscriber('/usb_cam/image_rect_color', Image, self.image_callback, queue_size =1)
		
	def image_callback(self,msg):
		image = self.ros_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		# image = self.ros_bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
		# image = self.ros_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
		#cv2.imshow("im",image)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (11, 11), 0)
		#cv2.imshow("blurred", blurred)
		cv2.waitKey(3)
		# thres = [[]]
		# thres = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)
		ret, thres = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)
		# print thres
		# thres = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)[1]
		# thresh = np.random.randint(2, size = image.shape)
		#cv2.imshow("thresh", thresh)
        # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (255,0,0), 2)
        print ("number of bright spots are" , len(contours))
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


		
if __name__ == '__main__':
	test = WayPoint()
	rospy.spin()