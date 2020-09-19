#!/usr/bin/env python

import rospy, actionlib, os, sys, time, math

from actionlib_msgs.msg import GoalStatusArray
from geometry_msgs.msg import PoseWithCovarianceStamped

POSE = [None, None]
LOOP = ""
TIMEOUT = 500

class NavigationTracker:

    def __init__(self, ground_truth, map_name):
        self.columns = ['id', 'map', 'map_generator', 'success', 'total_distance', 'start_time', 'end_time']
        self.database = self.open_csv(map_name) # File to write to
        self.map_name = map_name
        self.using_ground_truth = True if ground_truth.lower()=='true' else False
        self.runs = {} # Dict of the tracking dicts
        self.written = []

    def get_new_loop_dict(self):
        d = {}
        d['id'] = time.time()
        d['map'] = self.map_name
        d['map_generator'] = 'ground_truth' if self.using_ground_truth else 'openvslam'
        d['success'] = False
        d['total_distance'] = 0.0
        d['start_time'] = time.time()
        d['end_time'] = 0.0

        return d

    def append_run(self, run):
        self.runs.append(run)

    def open_csv(self, M):

        metrics_fp = os.path.join('/','home','conor','msc-project','openvslam','ros','src','navigation','metrics',M)
        if os.path.exists(metrics_fp):
            print('\t\t*Metrics file exists, opening to append.\n{}\n'.format(metrics_fp))
            metrics_csv = open(metrics_fp, 'a')

        else:
            print('\t\t*Metrics file doesnt exist, creating, writing columns.\n{}\n'.format(metrics_fp))
            metrics_csv = open(metrics_fp, 'w')
            metrics_csv.write(', '.join(self.columns )+'\n')

        return metrics_csv

    def write_results(self, loop):
        ordered = []
        for c in self.columns:
            ordered.append(self.runs[loop][c])

        if loop in self.runs:
            stringify = [str(v) for v in ordered]
            self.database.write(', '.join(stringify) + '\n')
            self.written.append(loop)
        # self.database.close()

    def close(self):
        self.database.close()
#___________________________End Class___________________________#

#################
#   Callbacks   #
#################

def status_callback(gsa, nav_tracker):
    global LOOP

    if len(gsa.status_list) == 0 :
        # Nothing to track.
        return
    
    # At least one goal sent --->
    elif LOOP == "":
        # First path.
        print('First loop received.')
        LOOP = gsa.status_list[-1].goal_id.id[:-2]
        d = nav_tracker.get_new_loop_dict()
        nav_tracker.runs[LOOP] = d
    
    # Loop has been initialized --->
    elif LOOP != gsa.status_list[-1].goal_id.id[:-2]:
        # New loop detected.
        print('New loop received.')
        LOOP = gsa.status_list[-1].goal_id.id[:-2]
        d = nav_tracker.get_new_loop_dict()
        nav_tracker.runs[LOOP] = d

    # Same loop  --->
    elif gsa.status_list[-1].status == 1:
        # Still tracking path
        #Check for timeout: 
        if (time.time() - nav_tracker.runs[LOOP]['start_time']) > TIMEOUT:
            print(time.time() - nav_tracker.runs[LOOP]['start_time'])
            nav_tracker.write_results()
            rospy.signal_shutdown('Navigation loop timed out')
        else:
            return

    # Not status of 1  --->
    elif gsa.status_list[-1].status == 3 and gsa.status_list[-1].goal_id.id[-1]  == '3':
        if LOOP not in nav_tracker.written:
            # Close
            print('Closing loop: {}'.format(LOOP))
            nav_tracker.runs[LOOP]['success'] = True
            nav_tracker.runs[LOOP]['end_time'] = time.time()
            nav_tracker.write_results(LOOP)
        


def pose_callback(pcs, nav_tracker):
    global POSE
    if POSE != [None, None] and LOOP != "":
        new_pose = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]
        nav_tracker.runs[LOOP]['total_distance'] += distance( POSE, new_pose)
        POSE = new_pose
    else:
        POSE = [pcs.pose.pose.position.x, pcs.pose.pose.position.y]


#################
#    General    #
#################

def distance(p1, p2):
    # on x, y axes
    x1, y1 = round(p1[0], 3), round(p1[1], 3)
    x2, y2 = round(p2[0], 3), round(p2[1], 3)

    x = (x2 - x1)**2
    y = (y2 - y1)**2
    
    return math.sqrt(x+y)


def main(nav_tracker):
    status_subscriber = rospy.Subscriber('/move_base/status', GoalStatusArray, status_callback, nav_tracker)
    pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, pose_callback, nav_tracker)

    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('navigation_evaluator', anonymous=True, disable_signals=True)

    try:
        map_name = sys.argv[1]
        using_truth = sys.argv[2]
    except Exception as e:
        print(e)
        print('Recieved: {}'.format(', '.join(sys.argv)))
        print('Usage: $python navigation_tracker.py map_name using_truth:=[true, false] (optional, def=300) timeout')
        exit()
    
    try:
        nav_tracker = NavigationTracker(using_truth, map_name)
        print('Listening for goals.')
    
        main(nav_tracker)
    except KeyboardInterrupt:
        print('Shutting down, closing file.')
        nav_tracker.close()


