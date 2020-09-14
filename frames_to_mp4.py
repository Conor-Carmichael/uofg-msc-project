import os, sys


def main(output__destination):   
    fps = 30
    os.system("ffmpeg -framerate {} \
    -pattern_type glob \
    -i '/~/msc-project/videos/frames/*.jpg' \
    -c:v libx264 {}".format(fps, output__destination))

    print("Finished.\nSaved to {}".format(output__destination))

if __name__=='__main__':
    if len(sys.argv) != 2 :
        print('Invalid input. Usage:')
        print('$python frames_to_mp4.py output_destination')

    main(sys.argv[1])