import os, sys


def main(video_name):
    command = "./openvslam/build/run_video_slam -v ./openvslam/build/orb_vocab/orb_vocab.dbow2 -m /home/conor/msc-project/Videos/{}.mp4 -c ./openvslam/build/msc-cam/config.yaml --frame-skip 1 --no-sleep --map-db ./openvslam/build/maps/{}.msg".format(video_name, video_name)
    os.system(command)

if __name__=='__main__':
    if len(sys.argv) != 2 :
        print('Invalid input. Usage:')
        print('$python vslam_video.py mp4_file_name')
        print('\nNote: Omit mp4 ext., map file will be saved to same file name.')

    main(sys.argv[1])