import os, sys



def main(out_file_name, run_slam):   

    print("Creating video.")
    os.system("ffmpeg -framerate 10 -pattern_type glob -i '/home/conor/camera_saves/frames/*.jpg' -c:v libx264 /home/conor/camera_saves/{}.mp4".format(out_file_name))
    print("Finished.\nSaved to /camera_saves/{}".format(out_file_name))

    if run_slam.lower() == 'y':
        
        os.system("cd .. && cd build")
        os.system("./run_video_slam -v ./orb_vocab/orb_vocab.dbow2 -m /home/conor/camera_saves/{}.mp4 -c ./msc-cam/config.yaml --frame-skip 3 --no-sleep --map-db {}.msg".format(out_file_name, out_file_name))

if __name__=='__main__':
    if len(sys.argv) != 2 :
        print('Invalid input. Usage:')
        print('$python create_video.py output_file_name')

    main(sys.argv[1], sys.argv[2])