#!/usr/bin/env python

import rospy, actionlib, os, sys, time, csv, math
import numpy as np 
# import pandas as pd 
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import PoseWithCovarianceStamped
# Reference for this code:
# https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-action-client-py.md


status = 0
pose = 0

#___________________________Move Base Client Class___________________________#

class MoveBaseClient:


    def __init__(self, goal_file):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.goals = self.get_goals(goal_file)
        
        # to store goal to retrieve from a list of goals
        self.goal_ind = 0                   


    def get_goals(self, file):
        # Read in the next goal pose. Set it up, return to send goal method.
        #FORMAT:
        #x, y;
        goal_list = []
        with open(file, 'r') as goals_file:
            goals_reader = csv.reader(goals_file, delimiter=',')
            for row in goals_reader:
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = "map"
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = float(row[0])
                goal.target_pose.pose.position.y = float(row[1])
                goal.target_pose.pose.orientation.w = 1.0

                goal_list.append(goal)

        return goal_list


    def send_goal(self, goal):
        self.client.send_goal(goal)
        

#___________________________End Class___________________________#

def distance(p1, p2):
    # on x, y axes
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    x = (x2 - x1)**2
    y = (y2 - y1)**2
    
    return math.sqrt(x+y)



def status_callback(gsa):
    global status
    if len(gsa.status_list) > 0:
        status = int(gsa.status_list[0].status)

def pose_callback(pcs):
    global pose
    pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]


def main(fp):
    rospy.init_node('navigation_controller', anonymous=True)
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback)
    pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)

    nav_client = MoveBaseClient(fp)
    # map_metrics = pd.read_csv(PATH, header=0)
    # columns = map_metrics.columns

    print("""
            Starting navigation goal evaulation.
            {} 2d Nav Goals to run.
        """.format( len(nav_client.goals)) )

    for g_num, g in enumerate(nav_client.goals):
        print("Executing Navigation Goal {}".format(g_num))
        nav_client.send_goal(g)

        start_pose = [0,0,0] #Logic doesnt work here on second + loop
        goal_pose = g
        last_pose = start_pose

        start_time = time.time()
        distance_total = 0.0

        while status != 3:
            distance_total += distance(round(last_pose, 4), round(pose, 4))
            last_pose = pose

        end_time = time.time() 

        print("""\n
            Time taken: {}
            Distance travelled: {}\n\n
        """.format(end_time-start_time, distance_total))


    print('\nAll navigation goals have been completed.\n')
   

if __name__ == '__main__':
    map_name = sys.argv[1]     
    fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','goal_sets', map_name+'.csv')
    main(fp)
