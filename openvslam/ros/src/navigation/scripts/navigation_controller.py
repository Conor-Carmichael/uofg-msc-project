#!/usr/bin/env python

import rospy, actionlib, os, sys, time, csv, math

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


def log_run_to_console(run_info):
    print(run_info)

def write_run_to_csv(map_name, run_info):
    with open('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format(map_name), 'w') as metrics_csv:
        writer = csv.writer(metrics_csv)
        writer.writerow(run_info.values())

def post_fail_logging(letters, run_log):
    for l in letters:
        # End of nav goal, add in the goal specific metrics:
        run_log['path_{}_failed'.format(l)] = 'n/a'
        run_log['path_{}_dist'.format(l)] =  'n/a'
        run_log['path_{}_time'.format(l)] = 'n/a'
        run_log['pos_{}'.format(l)] = 'n/a'


def status_callback(gsa):
    global status
    if len(gsa.status_list) > 0:
        status = int(gsa.status_list[-1].status)
    else:
        status = 0
    

def pose_callback(pcs):
    global pose
    pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]



def main(fp, map_name, is_ground_truth, timeout):
    rospy.init_node('navigation_controller', anonymous=True)
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback)
    pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)

    nav_client = MoveBaseClient(fp)

    run_log_helper = ['a','b','c','d'] #to help logging to the dict
    map_gen = 'ground_truth' if is_ground_truth.lower()=='true' else 'openvslam'
    run_log = {
        'map': map_name,
        'map_generator':map_gen,
        'start_pos': [0,0],
        'path_a_failed':None,
        'path_a_dist':None,
        'path_a_time':None,
        'end_pos_a':None,
        'path_b_failed':None,
        'path_b_dist':None,
        'path_b_time':None,
        'end_pos_b':None,
        'path_c_failed':None,
        'path_c_dist':None,
        'path_c_time':None,
        'end_pos_c':None,
        'path_d_failed':None,
        'path_d_dist':None,
        'path_d_time':None,
        'end_pos_d':None,
        'total_dist':None,
        'total_time': None
    }


    print("Starting navigation goal evaulation.\n{} 2d Nav Goals to run.".format( len(nav_client.goals)) )


    # Total loop tracking variables
    loop_start_time = time.time()
    loop_total_distance = 0.0

    last_pose = [0,0]

    ####################################################
    #
    #   Start of the loop for sending each intermediate navigation goal
    #
    ####################################################

    for goal_num, goal in enumerate(nav_client.goals):
        # Send goal, then enter 'wait for success' loop
        path_let = run_log_helper[goal_num]

        print("Executing Navigation Goal {}".format(path_let))
        nav_client.send_goal(goal)

        # Individual path tracking variables
        path_failed = False 
        path_start_time = time.time()
        path_distance_travelled = 0.0

        while status != 3:
            path_distance_travelled += distance(last_pose, pose)
            last_pose = pose

            if (time.time() - path_start_time) > timeout:
                print('Failed routine.')
                path_failed = True
                break

    

        # End of nav goal, add in the goal specific metrics:
        run_log['path_{}_failed'.format(path_let)] = path_failed
        run_log['path_{}_dist'.format(path_let)] =  None if path_failed else path_distance_travelled
        run_log['path_{}_time'.format(path_let)] = None if path_failed else time.time() - path_start_time
        run_log['end_pos_{}'.format(path_let)] = None if path_failed else last_pose

        #Accumulate distance metric
        run_total_distance += path_distance_travelled

        # If the navigation goal was failed, break out of for loop, and log others as N/A
        if path_failed:
            # Log the rest as n/a
            remaining = run_log_helper[goal_num+1:]
            post_fail_logging(remaining, run_log)
            break


    ####################################
    #
    #           Post Loop
    #
    ####################################
    print('\nAll navigation goals have been completed.\n')

    #Add full loop metrics to the run log:
    run_log['total_time'] = time.time() - loop_start_time
    run_log['total_dist'] = loop_total_distance


    print('Writing results...')
    write_run_to_csv(map_name, run_log)
    print("Results have been stored.")


   

if __name__ == '__main__':
    try: 
        map_name = sys.argv[1] 
        ground_truth = sys.argv[2]
    except IndexError as e:
        print('Usage: $python navigation_controller.py mapname using_ground_truth (optional- timeout, default 150)')

    timeout = 150
    try:
        timeout = sys.argv[3]
    except:
        print('Timeout defaulting to 120s.')
        
    fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','goal_sets', map_name+'.csv')
    main(fp, map_name, ground_truth, timeout)

