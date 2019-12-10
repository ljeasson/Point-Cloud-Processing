import os
import glob

from segment_pointcloud import process_point_cloud
from create_heightmap import create_heightmap, threshold

# Get list of point clouds to process
point_clouds = []
for file in os.listdir(os.getcwd()):
    if file.endswith(".las"):
        point_clouds.append(file)

base_point_cloud = point_clouds[0]
veg_point_cloud = point_clouds[1]
ground_point_cloud = point_clouds[2]

'''
# Segment Point Clouds into vegetation and ground
if __name__ == "__main__":
    # Convert LAZ to LAS
    #print("CONVERTING LAZ TO LAS")
    #os.system("laszip *.laz")
    #print("DONE\n")
    
    # Process point clouds
    for i in point_clouds:
        # Display full file name
        print("\nProcessing:",i)

        #print("LAS HEADER INFO")
        #os.system("lasinfo " + i)
        #print("DONE\n")

        # Get file name without ".las"
        fileName = i[:i.index(".")]
        print("File Name:",fileName)

        # Process point cloud
        process_point_cloud(fileName)
'''

# Create heightmap from Ground point cloud
create_heightmap(ground_point_cloud)