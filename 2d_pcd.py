"""
Copyright (c) 2019,
National Institute of Advanced Industrial Science and Technology (AIST),
All rights reserved.

This work is licensed under the terms of the 2-Clause BSD license.
For a copy, see <https://github.com/xdspacelab/openvslam/blob/master/LICENSE>.
"""


import sys
import msgpack
import json
import os

'''

Script taken from:
https://github.com/xdspacelab/openvslam/issues/87

edited to instead of just read the points, create a .pcd file 
to import to the Octomap Server.
-Conor

'''

def main(bin_fn, dest_fn):



    # Read file as binary and unpack data using MessagePack library
    with open(bin_fn, "rb") as f:
        data = msgpack.unpackb(f.read(), use_list=False)

    # The point data is tagged "landmarks"
    landmarks = data["landmarks"]
    print("Point cloud has {} points.".format(len(landmarks)))

    # Write point coordinates into file, one point for one line
    with open(dest_fn, "w") as f:
        #My addition
        pcd_file_header = "#.PCD v.7 - Point Cloud Data file format\nVERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {}\nDATA ascii\n".format(len(landmarks),len(landmarks))

        f.write(pcd_file_header)
        # end addition
        actual = 0
        for id, point in landmarks.items():
            pos = point["pos_w"]
            if pos[2] > -1.5 and pos[2] < 1.5:
                f.write("{} {} {}\n".format(pos[0], pos[1], pos[2]))
                actual += 1
    print("Finished, ", actual)
    # resp = raw_input('To view this file, type YES and press enter.\n')
    # if resp.upper() == 'YES':
    #     os.system("pcl_viewer -bc 1,1,1 -ps 2 -fc 0,0,0 /home/conor/msc-project/openvslam/build/maps/museum_capture.pcd ")


if __name__ == "__main__":
    argv = sys.argv

    if len(argv) < 3:
        print("Error, usage: ")
        # Edited prompt
        print("$python msc_to_pcd.py [map file] [.pcd destination]")

    else:
        bin_fn = argv[1]
        dest_fn = argv[2]
        main(bin_fn, dest_fn)