import os, sys


def main(args):
    mp4 = args[1]
    cam_config_file = args[2]
    msg_dest = args[3]
    
    command = "~/msc-project/openvslam/build/run_video_slam \
    -v ~/msc-project/openvslam/build/orb_vocab/orb_vocab.dbow2 \
    -m {} -c {} --frame-skip 1 \
    --no-sleep --map-db {}".format(mp4, cam_config_file, msg_dest)
    
    os.system(command)

if __name__=='__main__':
    if len(sys.argv) != 4:
        print('Invalid input. Usage:')
        print('$python vslam_video.py mp4_file camera_config_yaml msg_dest')

    main(sys.argv)