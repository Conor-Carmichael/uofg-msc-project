import sys, os

'''
This file is to run all the requisite scripts to create the 2 dimensional pcd for navigation maps.

Supplied to this must be the info required to properly name the files. See usage.

Sub-Scripts must take in a full file path, so this file makes full paths, passes to those scripts.

'''

def check_args(args):

    if len(args) != 2:
        print('Usage:\n$python map_pipeline.py \
            map:[easy, medium, hard] ')
        return False
    else:
        return True

def create_id(args):
    return "_".join(args[1:])

def log_process(pid):
    #This is hilariously python
    print("""
        #################################
        #
        #             Running
        #             {}
        #
        #################################
    """.format(pid))

def run_create_video(dest):
    os.system('python frames_to_mp4.py {}'.format(dest))

def run_openvslam(mp4, cam, msg_dest):
    os.system('python run_openvslam.py {} {} {}'.format(mp4, cam, msg_dest))

def run_pcd_conversion(msg_file, pcd_dest):
    os.system('python msg_to_pcd.py {} {}'.format(msg_file, pcd_dest))

def run_pcd_processing(pcd_file, two_dim_pcd_dest):
    os.system('python post_process_pcd.py {} {}'.format(pcd_file, two_dim_pcd_dest))



########
#      #
# MAIN #
#      #
########

def main(args):
    # Check the arguments for validity
    if not check_args(args):
        exit()
    map_id = create_id(args)
    base = os.path.join('~','msc-project')
    bot_type = sys.argv[1]


    # Create mp4 from frames folder
    mp4_save = os.path.join(base, 'videos', map_id+'.mp4')
    log_process('Frames to MP4')
    run_create_video(mp4_save)


    # Run OpenVSLAM
    map_msg_save = os.path.join(base, 'openvslam', 'build', map_id+'.msg') # Where to store openvslam output
    cam_config_file = os.path.join(base, 'openvslam','build', 'msc-cam', 'aal_cam.yaml')

    do = raw_input('Run OpenVSLAM? (y or n): ')
    while do.lower() == 'y': 
        run_openvslam(mp4_save, cam_config_file, map_msg_save)
        do = raw_input('\n\nRun openvslam again? (y or n): ')

    # Create pcd from message pack
    do = raw_input('Convert msg->pcd? (y or n): ')
    pcd_save = os.path.join(base, 'pcd', map_id+'.pcd') # Save msg conversion
    if do.lower() == 'y':
        log_process('Messagepack to point cloud')
        run_pcd_conversion(map_msg_save, pcd_save)

    # Run post processing on pcd
    do = raw_input('Run postprocessing on PCD file? (y or n): ')
    two_dim_pcd = os.path.join(base, 'pcd', '2d', map_id+'.pcd')
    if do.lower() == 'y':
        log_process('Post Processing PCD')
        run_pcd_processing(pcd_save, two_dim_pcd)

    # Finish
    return map_id



if __name__=='__main__':
   map_id =  main(sys.argv)
   print('Pipeline finished. The identifier is:\n{}'.format(map_id))