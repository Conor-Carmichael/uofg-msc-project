"""
Copyright (c) 2019,
National Institute of Advanced Industrial Science and Technology (AIST),
All rights reserved.

This work is licensed under the terms of the 2-Clause BSD license.
For a copy, see <https://github.com/xdspacelab/openvslam/blob/master/LICENSE>.
"""


import sys, os, re, math
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

def rotate_about_origin(p, rads):
    x, y = p[0], p[1]
    xx = x * math.cos(rads) + y * math.sin(rads)
    yy = -x * math.sin(rads) + y * math.cos(rads)

    return [xx, yy, p[2]]

def rotate_points(points):
    rotated = []
    for point in points:
        new_p = rotate_about_origin( [float(p) for p in point], 1.5708)
        rotated.append(new_p)
    return rotated


def rescale(points, scale_fact_x=3.75, scale_fact_y=4.00):
    resc = []
    for point in points:
        p = [float(v) for v in point]
        resc.append([p[0]*scale_fact_x,
            p[1]*scale_fact_y, 
            p[2]])

    return resc


def flattened(points):
    points = realign_axes(points) # Set the proper axes
    """Seems to be better to include all heights after a quick test""" 
    # index_mask = np.where((points[:, 2] < 1) & (points[:, 2] > -1 ))
    # filtered_points = points[index_mask] 
    flat = [ [p[0], p[1], 0.0] for p in points ]
    return flat


def distance(p1, p2):
    # on x, y axes
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    x = (x2 - x1)**2
    y = (y2 - y1)**2
    
    return math.sqrt(x+y)


def min_neighbor_filter(points, min_num_neighbors=5, radius=0.1):
    keep = []
    print('Filtering neighbors...')
    for ind, p in enumerate(points):
        neighbor_count = 0
        for n in points:
            # print(distance(p, n))
            if distance(p, n) <= radius:
                neighbor_count += 1
        # print("Neighbors: ", neighbor_count)
        if neighbor_count >= min_num_neighbors:
            keep.append(p)
        if ind % 200 == 0:
            print("point {}/{}".format(ind, len(points)))
    
    return keep



def save(points, name):
    header="VERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {}\nDATA ascii\n".format(len(points),len(points))
    
    with open(name, 'w') as f:
        f.write(header)
        for p in points:
            f.write("{} {} {}\n".format(p[0], p[1], p[2]) )
        f.close()
        print("Saved to {}".format(name))    

########################
# MAIN
#########################

def main(map_name, save_name, min_neighbors=None, radius=None):
    point_array = []
    with open(map_name, 'r') as pcd_file:
        point_array = get_point_list(pcd_file.readlines())
        pcd_file.close()


    point_array = flattened(point_array)
    filtered_points = min_neighbor_filter(point_array, min_num_neighbors=5, radius=0.07)

    print("Pre filter: {}\nPost filter: {}... {}% points removed.\n".format( len(point_array), len(filtered_points), 1-float((len(filtered_points)*1.0)/(len(point_array)*1.0)) )   )
    
    rotated = rotate_points(filtered_points)
    rescaled = rescale(rotated)

    save(rescaled, save_name)


if __name__ == "__main__":
    min_neighbors = None
    radius = None
    
    #
    try:
        map_name = sys.argv[1]  
        save_name = sys.argv[2]

    except:
        print("Usage:\n$python post_process_pcd.py map_name (optional->)min_neighbors (optional->)radius")
        exit()

    try:
        min_neighbors = sys.argv[3]
        radius = sys.argv[4]
    except:
        print("Min Neighbor and Radius not supplied, usage:\n$python post_process_pcd.py map_name (optional->)min_neighbors (optional->)radius\nContinuing with default values. ")

    main(map_name, save_name, min_neighbors=min_neighbors, radius=radius)