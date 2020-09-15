#!/usr/bin/env python

import rospy, actionlib, os, sys, time
import numpy as np 
# import pandas as pd 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray


def callback(info):
    # print(info.status_list.text)
    print(info)
   


if __name__ == '__main__':
    rospy.init_node('navigation_evaluator')
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, callback)
    rospy.spin()