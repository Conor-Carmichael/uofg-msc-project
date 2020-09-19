#!/usr/bin/env python

import rospy, actionlib, os, sys, time
import numpy as np 
# import pandas as pd 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray



def status_callback(gsa):
    global status
    
    if len(gsa.status_list) > 0:
        status = int(gsa.status_list[-1].status)
    else:
        status = 0

def pose_callback(pcs):
    global pose
    pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]



if __name__ == '__main__':
    rospy.init_node('navigation_evaluator')
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, callback)
    pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)

    rospy.spin()