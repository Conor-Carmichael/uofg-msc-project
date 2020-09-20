#!/usr/bin/env python

import rospy, actionlib, os, sys, time, csv, math

from actionlib_msgs.msg import GoalStatusArray
from  move_base_msgs.msg import MoveBaseActionGoal, MoveBaseGoal
from std_msgs.msg import Header
from actionlib_msgs.msg import GoalID

# References for this code:
# [1] https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-action-client-py.md
# [2] https://python.hotexamples.com/examples/move_base_msgs.msg/MoveBaseActionGoal/-/python-movebaseactiongoal-class-examples.html
# [1] Was used first, but the ActionLib is bugged for what I need on this python version. Structue/idea adopted.
# [2] Was used to get examples of using the MoveBaseActionGoal, GoalID, and MoveBaseGoal objects.

#___________________________NavigationController Class___________________________#

SHUTDOWN_REASON ='Successful termination of goal set.'
LAST_GOAL = 'NONE'

class NavigationController:

    def __init__(self, goal_file):
        self.client = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)
        while self.client.get_num_connections() == 0 :
            continue 
        print("Client connected.")
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
            # for i in range(5):

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

        if self.current_goal < len(self.goals):
            goal = self.goals[self.current_goal]

            self.client.publish(goal)
            print('Sending goal \n{}'.format(goal) )

            self.current_goal += 1

            return goal.goal_id.id
        else:
            rospy.signal_shutdown(SHUTDOWN_REASON)

#____________________________________________________#

def status_callback(gsa, nav_controller):
    global LAST_GOAL
    try: 
        if gsa.status_list[-1].goal_id.id == LAST_GOAL and gsa.status_list[-1].status == 3 :
            LAST_GOAL = nav_controller.send_goal()
        else:
            rospy.sleep(0.2)
            return
    except Exception as e:
        # First time will have an error
        if LAST_GOAL == 'NONE':
            LAST_GOAL = nav_controller.send_goal()

        
    
def main(goal_fp):
    global LAST_GOAL

    rospy.init_node('navigation_controller', anonymous=True, disable_signals=True)

    nav_controller = NavigationController(goal_fp)
    
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback, nav_controller)

    rospy.spin()


if __name__ == '__main__':
    map_name = sys.argv[1]
    goal_fp = os.path.join('/','home', 'conor','msc-project', 
                            'openvslam','ros','src','navigation',
                            'goal_sets', map_name+'.csv')

    main(goal_fp)
