import csv, os
import pandas as pd

if __name__ =='__main__':
    cols = ['time_run', 'map', 'map_generator', 
        'path_a_failed', 'path_a_dist', 'path_a_time', 
        'path_b_failed', 'path_b_dist', 'path_b_time', 
        'path_c_failed', 'path_c_dist', 'path_c_time', 
        'path_d_failed', 'path_d_dist', 'path_d_time', 
        'total_dist', 'total_time']


    if os.path.exists('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format('easy_loop')):
        print('Exists, opening to append.')
        csv = open('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format('easy_loop'), 'a')
    else:
        print('Doesnt exist, establishing adding cols')
        csv = open('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format('easy_loop'), 'w')
        csv.write(', '.join(cols)+'\n')

    # try: 
    #     csv = open('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format('easy_loop'), 'a')
    #     # print(csv.readlines())
    #     print('\t\t*Loaded metrics dataframe*')
    # except:
    #     print('\t\t*Metrics dataframe for this map not found. Creating new dataframe*')
    
    #     metrics_df = pd.DataFrame(columns=cols)


    new_row = ['32163231', 'easy', 'truth','False', '2.232', '12.11','False', '2.87', '32.332','False', '2.997', '64.332','False', '4.87', '41.332', '12', '1125.32']
    csv.write(', '.join(new_row)+'\n')
    # temp_df = pd.DataFrame(new_row, columns=cols)

    # metrics_df.to_csv('/home/conor/msc-project/openvslam/ros/src/navigation/metrics/{}.csv'.format('easy_loop'))    