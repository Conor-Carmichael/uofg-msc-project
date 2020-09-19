#!/usr/bin/env python

import rospy, actionlib, os, sys, time, csv, math

from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
# Reference for this code:
# Made my own publisher, but followed this setup
# https://github.com/HotBlackRobotics/hotblackrobotics.github.io/blob/master/en/blog/_posts/2018-01-29-action-client-py.md


status = 0
pose = 0

#___________________________Move Base Client Class___________________________#
class MoveBaseClient:

    def __init__(self, goal_file):
        self.client = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.goals = self.get_goals(goal_file)


    def get_goals(self, file):
        # Read in the next goal pose. Set it up, return to send goal method.
        #FORMAT:
        #x, y;
        goal_list = []
        with open(file, 'r') as goals_file:
            goals_reader = csv.reader(goals_file, delimiter=',')
            for row in goals_reader:
                goal = PoseStamped()
                goal.header.frame_id = "map"
                goal.header.stamp = rospy.Time.now()
                goal.pose.position.x = float(row[0])
                goal.pose.position.y = float(row[1])
                goal.pose.orientation.w = 1
                print(goal)
                goal_list.append(goal)

        return goal_list


    def send_goal(self, goal): 
        self.client.publish(goal)
        

#___________________________End Class___________________________#


#################
#   General     #
#################


def distance(p1, p2):
    # on x, y axes
    x1, y1 = round(p1[0], 3), round(p1[1], 3)
    x2, y2 = round(p2[0], 3), round(p2[1], 3)

    x = (x2 - x1)**2
    y = (y2 - y1)**2
    
    return math.sqrt(x+y)


def log_run_to_console(run_info):
    print(run_info)


def post_fail_logging(letters, run_log):
    for l in letters:
        # End of nav goal, add in the goal specific metrics:
        run_log['path_{}_failed'.format(l)] = 'n/a'
        run_log['path_{}_dist'.format(l)] =  'n/a'
        run_log['path_{}_time'.format(l)] = 'n/a'
        run_log['pos_{}'.format(l)] = 'n/a'

def sort_values_by_cols(cols, dict):
    ret_arr = []
    for col in cols:
        ret_arr.append(dict[col])
    return ret_arr


#################
#   Callbacks   #
#################

def status_callback(gsa):
    global status
    
    if len(gsa.status_list) > 0:
        status = int(gsa.status_list[-1].status)
    else:
        status = 0
    

def pose_callback(pcs):
    global pose
    pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]



def main(goals_fp, metrics_fp, map_name, is_ground_truth, timeout):

    #####################################################################
    #                                                                   #
    #   Setup for run: Reading/creating metric file, setting up logging #
    #                                                                   #
    #####################################################################

    global status 

    rospy.init_node('navigation_controller', anonymous=True)
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback)
    pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback)
    rospy.spin()

    
    cols = ['time_run', 'map', 'map_generator', 
        'path_a_failed', 'path_a_dist', 'path_a_time', 
        'path_b_failed', 'path_b_dist', 'path_b_time', 
        'path_c_failed', 'path_c_dist', 'path_c_time', 
        'path_d_failed', 'path_d_dist', 'path_d_time', 
        'total_dist', 'total_time']

    if os.path.exists(metrics_fp):
        print('\t\t*Metrics file exists, opening to append.\n')
        csv = open(metrics_fp, 'a')
    else:
        print('\t\t*Metrics file doesnt exist, creating, writing columns.\n')
        csv = open(metrics_fp, 'w')
        csv.write(', '.join(cols)+'\n')


    nav_client = MoveBaseClient(goals_fp)

    run_log_helper = ['a','b','c','d'] #to help logging to the dict
    map_gen = 'ground_truth' if is_ground_truth.lower()=='true' else 'openvslam'

    run_log = {
        'map': map_name,
        'map_generator':map_gen,
    }
    print("\t\t*Based on {} map of {}\n".format(map_gen, map_name))


    print("-_____Running {} 2d Nav Goals______-\n\n".format( len(nav_client.goals)) )

    # Total loop tracking variables
    loop_start_time = time.time()
    loop_total_distance = 0.0
    # To calculate distance each step
    last_pose = [0,0]


    #####################################################################
    #                                                                   #
    #   Start of the loop for sending each intermediate navigation goal #
    #                                                                   #
    #####################################################################
    
    for goal_num, goal in enumerate(nav_client.goals):

        path_let = run_log_helper[goal_num] #just gets letter assoc with the path.

        print("---Executing Navigation Goal {}".format(path_let))


        nav_client.send_goal(goal)

        # Individual path tracking variables
        path_failed = False 
        path_start_time = time.time()
        path_distance_travelled = 0.0

        while status != 3:

            if (time.time() - path_start_time) > timeout:
                print('Failed routine.')
                path_failed = True
                print("Navigation Goal {} failed. Breaking, logging.".format(path_let))
                break
            else:
                path_distance_travelled += distance(last_pose, pose)
                last_pose = pose

        #Status <-- 3; Means nav complete. 
        #Need to manually set. Proceeds to fast for the subscriber to get the new value.
        status = 0
    

        # End of nav goal, add in the path specific metrics:
        run_log['path_{}_failed'.format(path_let)] = path_failed
        run_log['path_{}_dist'.format(path_let)] =  'None' if path_failed else path_distance_travelled
        run_log['path_{}_time'.format(path_let)] = 'None' if path_failed else time.time() - path_start_time

        #Accumulate distance metric
        loop_total_distance += path_distance_travelled

        # If the navigation goal was failed, break out of for loop, and log others as N/A
        if path_failed:
            # Log the rest as n/a
            remaining = run_log_helper[goal_num+1:]
            post_fail_logging(remaining, run_log)
            break


    #####################################################################
    #                                                                   #
    #                        Post Loop                                  #
    #                                                                   #
    #####################################################################
    
    run_log['time_run'] = loop_start_time    
    run_log['total_time'] = time.time() - loop_start_time
    run_log['total_dist'] = loop_total_distance

    print('\nAll navigation goals have been completed.\nWriting results...')
    new_row = sort_values_by_cols(cols, run_log)
    new_row = [str(v) for v in new_row]
    csv.write(', '.join(new_row)+'\n')

    print("Results have been stored.")

    # nav_client.cancel()
    csv.close()

#----------------------------------------- End of main(...) -----------------------------------------#



# Runner: deals with terminal args
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
        print('\t\t*Timeout defaulting to 150s')
        
    goal_fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','goal_sets', map_name+'.csv')
    metrics_fp = os.path.join('/','home', 'conor','msc-project', 'openvslam','ros','src','navigation','metrics', map_name+'.csv')

    main(goal_fp, metrics_fp, map_name, ground_truth, timeout)

