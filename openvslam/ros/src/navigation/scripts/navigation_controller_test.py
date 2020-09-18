#!/usr/bin/env python

import rospy, actionlib, os, sys, time, csv, math

from actionlib_msgs.msg import GoalStatusArray
from  move_base_msgs.msg import MoveBaseActionGoal, MoveBaseGoal
from std_msgs.msg import Header
from actionlib_msgs.msg import GoalID

# Reference for this code:
# Made my own publisher, but followed this setup
# https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-action-client-py.md

#___________________________Move Base Client Class___________________________#

SHUTDOWN_REASON ='Successful termination of goal set.'
LAST_GOAL = 'NONE'

class NavigationController:

    def __init__(self, goal_file):
        self.client = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)
        self.goals = self.get_goals(goal_file)
        self.current_goal = 0


    def get_goals(self, file):
        # Read in the next goal pose. Set it up, return to send goal method.
        #FORMAT:
        #x, y;
        run_identfier = time.time()

        goal_list = []
        with open(file, 'r') as goals_file:
            goals_reader = csv.reader(goals_file, delimiter=',')
            for row_num, row in enumerate(goals_reader):

                MBAG = MoveBaseActionGoal()
                MBAG.goal_id = GoalID()
                MBAG.goal_id.id = str(run_identfier)+"_path_"+str(row_num)

                MBAG.header = Header()
                MBAG.header.frame_id = 'map'

                MBG = MoveBaseGoal()
                MBG.target_pose.header.frame_id = "map"
                MBG.target_pose.pose.position.x = float(row[0])
                MBG.target_pose.pose.position.y = float(row[1])
                MBG.target_pose.pose.orientation.w = 1.0

                MBAG.goal = MBG

                goal_list.append(MBAG)

        return goal_list


    def send_goal(self): 
        global UPDATING

        if self.current_goal < len(self.goals):
            goal = self.goals[self.current_goal]
            print('Sending goal {} @{}....{}'.format(self.current_goal, time.time(), UPDATING) )
            self.client.publish(goal)

            self.current_goal += 1

            return goal.goal_id.id
        else:
            rospy.signal_shutdown(SHUTDOWN_REASON)

#____________________________________________________#

def status_callback(gsa, nav_controller):
    global LAST_GOAL

    if len(gsa.status_list) == 0 :
        LAST_GOAL = nav_controller.send_goal()

    elif gsa.status_list[-1].status == 3 and gsa.status_list[-1].goal_id == LAST_GOAL :
        LAST_GOAL = nav_controller.send_goal()

    elif gsa.status_list[-1].status == 3 and gsa.status_list[-1].goal_id != LAST_GOAL :
        return
    
    

    
def main(goal_fp):
    rospy.init_node('navigation_controller', anonymous=True, disable_signals=True)

    nav_controller = NavigationController(goal_fp)
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback, nav_controller)

    rospy.spin()


if __name__ == '__main__':
    map_name = sys.argv[1]
    goal_fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','goal_sets', map_name+'.csv')

    main(goal_fp)
