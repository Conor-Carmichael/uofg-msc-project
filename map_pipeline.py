import sys, os

'''
This file is to run all the requisite scripts to create the 2 dimensional pcd for navigation maps.

Supplied to this must be the info required to properly name the files. See usage.

Sub-Scripts must take in a full file path, so this file makes full paths, passes to those scripts.

'''

def check_args(args):

    if len(args) != 4:
        print('Usage:\n$python map_pipeline.py bot_name:[aal, sc] map:[museum, alley] mapping_type:[quick, long] ')
        return False
    else:
        return True

def create_id(args):
    bot = args[1]
    map_name = args[2]
    mapping_type = args[3]
    i = "{}_{}_{}".format(bot, map_name, mapping_type)
    return i

def run_create_video(dest):
    os.system('python frames_to_mp4.py {}'.format())

def run_openvslam(mp4, cam, msg_dest):
    os.system('python vslam_video.py {} {} {}'.format(mp4, cam, msg_dest))





def main(args):
    # Check the arguments for validity
    if not check_args(args):
        exit()
    map_id = create_id(args)
    base = os.path.join('~','msc-project')
    bot_type = sys.argv[1]


    # Create mp4 from frames folder
    mp4_save = os.path.join(base, 'videos', map_id+'.mp4')
    run_create_video(mp4_save)


    # Run OpenVSLAM
    map_msg_save = os.path.join(base, 'msgs', map_id+'.msg')
    cam_config_file = os.path.join(base, 'openvslam','build', 'msc-cam', bot_type+'_cam.yaml')
    retry = 'y'
    while retry.lower() == 'y': 
        run_openvslam(mp4_save, cam_config_file, map_msg_save)
        retry = raw_input('\n\nRun openvslam again? (y or n): ')


    # Create pcd from message pack
    pcd_save = os.path.join(base, 'pcd', map_id+'.pcd')

    # Run post processing on pcd

    # Finish

if __name__=='__main__':
    main(sys.argv)