#!/usr/bin/env python
from __future__ import print_function

import roslib, os
# roslib.load_manifest('my_package')

from std_msgs.msg import String
from sensor_msgs.msg import Image
import rospy, math, sys, message_filters, os
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

import time


def callback(image):
    image_pub = rospy.Publisher("/camera/image_raw", Image, queue_size=10)
    bridge = CvBridge()

    try:
        cv_image = bridge.imgmsg_to_cv2(image, "bgr8") #Convert the images

    except CvBridgeError as e:
        print(e)

    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'videos', 'frames', 'frame_{}.jpg'.format(time.time())), cv_image)

    image_pub.publish(image)



def feed_subscriber():

    rospy.init_node('image_converter', anonymous=True)
    print("Camera feed subscriber node created.")

    print("Clearing the previous camera frames.")
    os.system('rm -r ~/msc-project/videos/frames/*')

    cam_one = "/sc_bot/camera1/image_raw"

    rospy.Subscriber(cam_one, Image, callback)

    rospy.spin()


if __name__ == '__main__':
    feed_subscriber()




