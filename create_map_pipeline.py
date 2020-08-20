import os, sys, msgpack, json

# Links together functionality from stills to mapping

def create_video():
    
    pipeline_file_name = raw_input('Name for files in this pipeline: ')
    
    print("""
    #########################
    #                       #
    #       Creating .mp4   #
    #                       #
    #########################
    """)

    fps=30 # Same as openvslam/build/msc-cam/config.yaml

    ffpmeg_cmd = "ffmpeg -framerate {} -pattern_type glob -i \
    '/home/conor/msc-project/Videos/frames/*.jpg' -c:v \
    libx264 /home/conor/msc-project/Videos/{}.mp4".format(fps, pipeline_file_name)

    print("#####################\n\tCreating {}.mp4\n#####################".format(pipeline_file_name))

    os.system(ffpmeg_cmd)
    return pipeline_file_name



def run_vslam(pipeline_file_name):

    print("""
    #########################
    #                       #
    #       Running VSlam   #
    #                       #
    #########################
    """)

    command = "./openvslam/build/run_video_slam \
    -v ./openvslam/build/orb_vocab/orb_vocab.dbow2 \
    -m /home/conor/msc-project/Videos/{}.mp4 \
    -c ./openvslam/build/msc-cam/config.yaml \
    --frame-skip 1 --no-sleep \
    --map-db ./openvslam/build/maps/{}.msg".format(pipeline_file_name, pipeline_file_name)
    os.system(command)
   



# Script taken from:
# https://github.com/xdspacelab/openvslam/issues/87

# edited to instead of just read the points, create a .pcd file 
# to import to the Octomap Server.
# -Conor
def create_pcd(map_file_name):

    print("""
    #########################
    #                       #
    #       Creating .pcd   #
    #                       #
    #########################
    """)


    cwd = os.getcwd()
    maps_path = os.path.join(cwd, 'openvslam','build','maps')

    message_pack_file = os.path.join(maps_path, map_file_name+'.msg')

    with open(message_pack_file, "rb") as f:
        data = msgpack.unpackb(f.read(), use_list=False)

    landmarks = data["landmarks"]
    print("Point cloud has {} points.".format(len(landmarks)))

    pcd_file = os.path.join(maps_path, map_file_name+'.pcd')

    with open(pcd_file, "w") as f:

        pcd_file_header = "#.PCD v.7 - Point Cloud Data file format\nVERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {}\nDATA ascii\n".format(len(landmarks),len(landmarks))
        f.write(pcd_file_header)

        for id, point in landmarks.items():
            pos = point["pos_w"]
            f.write("{} {} {}\n".format(pos[0], pos[1], pos[2]))

    return pcd_file



def post_process_pcd(fname):
    print("""
    #########################
    #                       #
    #     Processing .pcd   #
    #                       #
    #########################
    """)
    os.system("python post_process_pcd.py {}".format(fname))


def main():

    pipeline_file_name = create_video()

    rerun = True
    while rerun:
        run_vslam(pipeline_file_name)
        rerun = True if raw_input('Retry OpenVSlam? (y or n): ').lower() == 'y' else False

    pcd_file_path = create_pcd(pipeline_file_name)

    post_process_pcd(pipeline_file_name)

    # view_file = raw_input('View the 2d .pcd file now? (y or n): ')

    # if view_file.lower() == 'y':
    #     os.system("pcl_viewer -bc 0,0,0 -fc 0,255,0  {}".format(pcd_file_path))
    # else:
    #     print('Script finished.')




if __name__ == "__main__":
    main()
    print("\n\nScript finished.")
    print("View the Point Cloud Data by running:\npcl_viewer ~/filepath\n")
    print("View the map by roslaunch-ing the octomapping package, and oct_l launch file.")
