#!/usr/bin/python

import os
import glob
import sys, getopt

from segment_pointcloud import segment_point_cloud
from create_heightmap import create_heightmap

def main(argv):
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    
    input_point_cloud = ''
    header = False

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('USAGE: process_pointcloud.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('USAGE: process_pointcloud.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_point_cloud = arg
        elif opt == "-header":
            header = True

    #if not input_point_cloud.endswith(".las"):
    #    print('Incorrect file format\nUse .las or .laz point clouds')
    #    sys.exit()
    
    print('Input point cloud: ', input_point_cloud, '\n')

    # Convert LAZ to LAS
    if input_point_cloud.endswith(".laz"):
        print("Converting",input_point_cloud,"to LAS")
        os.system("laszip -i " + str(input_point_cloud))
        print("DONE\n")

    # Get header info if enabled
    if header: os.system("lasinfo -i " + str(input_point_cloud) + " -o header_info.txt")
    
    # Get point cloud file name without ".las"
    fileName = input_point_cloud[:input_point_cloud.index(".")]
 
    # Segment Point Clouds into vegetation and ground
    segment_point_cloud(input_point_cloud, fileName)
    
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
    

if __name__ == "__main__":
   main(sys.argv[1:])