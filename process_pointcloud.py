#!/usr/bin/python

import os
import glob
import sys, getopt

from segment_pointcloud import segment_point_cloud
from create_heightmap import create_heightmap
from merge_tiles import merge_tiles

def main(argv):
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    
    directory = ''
    header = False

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('USAGE: process_pointcloud.py -i <input file or directory>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('USAGE: process_pointcloud.py -i <input file or directory>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            directory = arg
        elif opt == "-header":
            header = True

    # If input ends with .laz
    if directory.endswith(".laz"):
        print('Incorrect file format\nUse .las or .laz point clouds')
        sys.exit()
    
    print('Input: ', directory, '\n')

    # IF INPUT IS A POINT CLOUD
    if directory.endswith(".las"):
        # Get point cloud file name without ".las"
        directory_no_ext = directory[ : directory.index(".")]

        # Segment Point Cloud into vegetation and ground
        segment_point_cloud(directory, directory_no_ext)
    
    # IF INPUT IS A DIRECTORY
    else:
        merged_directory = ""

        # Merge directory of tiles
        merge_tiles(directory, 0.5)

        for dirpath,_,filenames in os.walk(directory+"\merged"):
            for f in filenames:
                merged_directory = os.path.abspath(os.path.join(dirpath, f))
        
        merged_directory_no_ext = merged_directory[: merged_directory.index(".")]
        print(merged_directory_no_ext)

        # Segment Point Clouds into vegetation and ground
        segment_point_cloud(merged_directory, merged_directory_no_ext)
    
    '''
    # Get list of point clouds to process
    point_clouds = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".las"):
            point_clouds.append(file)
 
    base_point_cloud = point_clouds[0]
    ground_point_cloud = point_clouds[1]
    veg_point_cloud = point_clouds[2]
    
    # Create heightmap from Ground point cloud
    fileName_ground = input_point_cloud[:input_point_cloud.index(".")]
    #create_heightmap(ground_point_cloud, fileName_ground)
    '''
    
    # Open UE4 Editor with PCM Pipeline
    print("OPENING UE4 EDITOR WITH PCM PIPELINE")
    #os.system("UE4Editor 'D:\Users\Lee\Unreal Projects\PCM_PIpeline_v2\PCM_PIpeline_v2.uproject'")
    print("DONE\n")


if __name__ == "__main__":
    main(sys.argv[1:])