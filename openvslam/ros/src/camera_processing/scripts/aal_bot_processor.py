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

def save_individual_frames(o, t, th, f):

    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'Videos', 'frames','one', 'frame_{}.jpg'.format(time.time())), o)
    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'Videos', 'frames','two', 'frame_{}.jpg'.format(time.time())), t)
    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'Videos', 'frames','three', 'frame_{}.jpg'.format(time.time())), th)
    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'Videos', 'frames','four', 'frame_{}.jpg'.format(time.time())), f)

def callback(cam_one, cam_two, cam_three, cam_four):
    # 1 +x, 2 +y, 3 -x, 4 -y
    image_pub = rospy.Publisher("/camera/image_raw", Image, queue_size=10)
    bridge = CvBridge()

    try:
        cv_images = []
        for image in [cam_one, cam_two, cam_three, cam_four]:
            cv_image = bridge.imgmsg_to_cv2(image, "bgr8") #Convert the images
            cv_images.append(cv_image)

    except CvBridgeError as e:
        print(e)

    height, width = cv_images[2].shape[:2] # 2 = cam three -x
    half = width // 2
    to_split = cv_images[2]
    l, r = to_split[:, :half], to_split[:, half:] # Split the back facing camera

    ordered = (r, cv_images[1], cv_images[0], cv_images[3], l  ) #Create tuple to stack

    to_pub = np.concatenate(ordered, axis=1)

    cv2.imwrite(os.path.join('/', 'home', 'conor', 'msc-project', 'videos', 'frames', 'frame_{}.jpg'.format(time.time())), to_pub)

    # save_individual_frames( cv_images[0], cv_images[1], cv_images[2], cv_images[3])

    to_pub = bridge.cv2_to_imgmsg(to_pub, "bgr8") # Necessary encoding
    image_pub.publish(to_pub)



def feed_subscriber():

    rospy.init_node('image_converter', anonymous=True)

    print("Clearing the previous camera frames.")
    os.system('rm -r /home/conor/msc-project/videos/frames/*')
    print("Clearing the previous camera frames complete.")

    cam_one = "/aal_bot/camera1/image_raw"
    cam_two = "/aal_bot/camera2/image_raw"
    cam_three = "/aal_bot/camera3/image_raw"
    cam_four = "/aal_bot/camera4/image_raw"

    image_sub_one = message_filters.Subscriber(cam_one, Image)
    image_sub_two = message_filters.Subscriber(cam_two, Image)
    image_sub_three = message_filters.Subscriber(cam_three, Image)
    image_sub_four = message_filters.Subscriber(cam_four, Image)



    time_synch = message_filters.TimeSynchronizer([
                                                image_sub_one,
                                                image_sub_two,
                                                image_sub_three,
                                                image_sub_four
                                                ], 10)
    time_synch.registerCallback(callback)

    rospy.spin()


if __name__ == '__main__':
    feed_subscriber()




