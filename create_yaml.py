import time, sys, os


if __name__ == '__main__':
    map_name = sys.argv[1]

    os.system('source /home/conor/msc-project/openvslam/ros/devel/setup.bash')
    
    command = 'roslaunch gazebo_env create_yaml map:={}'.format(map_name)
    os.system(command)

    time.sleep(7)


