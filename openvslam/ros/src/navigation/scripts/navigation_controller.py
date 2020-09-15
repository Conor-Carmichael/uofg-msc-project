#!/usr/bin/env python

import rospy, actionlib, os, sys, time
import numpy as np 
# import pandas as pd 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray

# Reference for this code:
# https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-action-client-py.md



class MoveBaseClient:


    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        
        # to store goal to retrieve from a list of goals
        self.goal_ind = 0                   


    def get_next_goal(self, index):
        # Read in the next goal pose. Set it up, return to send goal method.

        return ''


    def send_goal(self, goal):
        self.client.send_goal(goal)
        wait = self.client.wait_for_result()

        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        
        else:
            return_tup = (start, time.time(), self.client.get_result())
            return return_tup


    def callback(self):
        if len(gsa.status_list) > 0:
            status = int(gsa.status_list[0].status)
            print(status)

        



def main():
    rospy.init_node('navigation_controller', anonymous=True)
    nav_client = MoveBaseClient()

    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, nav_client.callback)
    
    goal = MoveBaseGoal()

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = 2
    goal.target_pose.pose.position.y = 0

    goal.target_pose.pose.orientation.w = 1.0

    res = nav_client.send_goal(goal)



    rospy.spin()




    


if __name__ == '__main__':

    main()
