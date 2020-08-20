"""
Copyright (c) 2019,
National Institute of Advanced Industrial Science and Technology (AIST),
All rights reserved.

This work is licensed under the terms of the 2-Clause BSD license.
For a copy, see <https://github.com/xdspacelab/openvslam/blob/master/LICENSE>.
"""


import sys, os, re
import numpy as np


def realign_axes(points):
    # Swaps incoming Z axis to be the Y axis. Visuzalizing the pcd before this would have the floor be on the x-z plane. More normal to have it on the x-y
    return np.array([ [p[0], p[2], p[1]] for p in points])


def get_point_list(lines):
    points = []
    for line_num, line in enumerate(lines):
        float_reg = r"-?\d\.\d\d"
        floats = re.findall(float_reg, line) 
        if len(floats) > 0:
            point = [float(f) for f in floats]
            points.append(point)

    return np.array(points)


def flattened(points):
    index_mask = np.where((points[:, 1] < 1) & (points[:, 1] > -1 ))
    
    filtered = points[index_mask] 
    flat = realign_axes(filtered) # Set the proper axes

    return flat


def rotate_plane(points):
    rotated = []
    return rotated


def discretize(points):
    x_bound = [np.min(points[:,0]), np.max(points[:,0])]
    y_bound = [np.min(points[:,1]), np.max(points[:,1])]


def save(points, name):
    save_path = os.path.join(os.getcwd(), 'openvslam','build','maps', name+'_2d.pcd')

    header="VERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {}\nDATA ascii\n".format(len(points),len(points))
    with open(save_path, 'w') as f:
        f.write(header)
        for p in points:
            f.write("{} {} {}\n".format(p[0], p[1], p[2]) )
        f.close()




def main(map_name):
    
    with open(os.path.join(os.getcwd(), 'openvslam','build','maps',map_name+'.pcd'), 'r') as pcd_file:
        point_array = get_point_list(pcd_file.readlines())
        bounds = []

        flat = flattened(point_array)

        save(flat, map_name)
        
    


if __name__ == "__main__":
    map_name = sys.argv[1]  

    main(map_name)