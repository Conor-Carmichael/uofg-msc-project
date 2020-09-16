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
    x1, y1 = round(p1[0], 3), round(p1[1], 3)
    x2, y2 = round(p2[0], 3), round(p2[1], 3)

    x = (x2 - x1)**2
    y = (y2 - y1)**2
    
    return math.sqrt(x+y)



def status_callback(gsa):
    global status
    if len(gsa.status_list) > 0:
        status = int(gsa.status_list[-1].status)
    else:
        status = 0
    

def pose_callback(pcs):
    global pose
    pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]



def main(fp, timeout):
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


    # start_pose = [0,0,0] #Logic doesnt work here on second + loop
    last_pose = [0,0]

    for g_num, g in enumerate(nav_client.goals):
        print("Executing Navigation Goal {}".format(g_num))
        nav_client.send_goal(g)

        failed = False
        goal_pose = g

        start_time = time.time()
        path_distance = 0.0

        while status != 3:
            path_distance += distance(last_pose, pose)
            last_pose = pose

            if (time.time() - start_time) > timeout:
                print('Failed routine.')
                failed = True
                break

        end_time = time.time() 

        print("""\n

            Path {}
            {} ----> {}
            x: {}--> {}
            y: {}--> {}

            Time taken: ............{}s
            Distance travelled: ....{}m\n\n
        """.format( "Failed" if failed else "Completed",
                    g_num, g_num+1, 
                    nav_client.goals[g_num-1].target_pose.pose.position.x, g.target_pose.pose.position.x,
                    nav_client.goals[g_num-1].target_pose.pose.position.y, g.target_pose.pose.position.y,
                    end_time-start_time, path_distance))


    print('\nAll navigation goals have been completed.\n')
   

if __name__ == '__main__':
    map_name = sys.argv[1] 
    ground_truth = sys.argv[2]
    timeout = 150
    try:
        timeout = sys.argv[3]
    except:
        print('Timeout defaulting to 120s.')
    fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','goal_sets', map_name+'.csv')
    main(fp, timeout)
