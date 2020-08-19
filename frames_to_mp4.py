import os, sys


def main(out_file_name):   
    fps = 30
    print("Creating video @{} FPS.".format(fps))
    os.system("ffmpeg -framerate {} -pattern_type glob -i '/home/conor/msc-project/Videos/frames/*.jpg' -c:v libx264 /home/conor/msc-project/Videos/{}.mp4".format(fps, out_file_name))
    print("Finished.\nSaved to msc-project/Videos/{}".format(out_file_name))

if __name__=='__main__':
    if len(sys.argv) != 2 :
        print('Invalid input. Usage:')
        print('$python create_video.py output_file_name')

    main(sys.argv[1])