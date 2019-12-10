import os
import random
from PIL import Image

def get_index_positions(listOfElements, element):
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = listOfElements.index(element, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError as e:
            break
    return indexPosList

def get_lasheader_info(pc):
    header_info = []
    os.system("lasinfo -i " + pc + " -o info.txt")
    file = open("info.txt", "r")
    info = file.read()
    info = info.split("\n")
    for i in info:
        i = i.split(' ')
        #blank_indices = get_index_positions(i, '')
        i = [e for e in i if e not in ('')]
        header_info.append(i)
    return header_info

def count_points(info):
    num_ground=num_veg = 0
    for i in info:
        if 'ground' in i:
            num_ground = int(i[0])
        if 'vegetation' in i:
            num_veg = int(i[0])
    num_points = num_ground + num_veg
    return num_points

def get_boundaries(info):
    minx=maxx=miny=maxy=minz=maxz = 0
    for i in info:
        if 'X' in i:
            minx = int(i[1])
            maxx = int(i[2])
        if 'Y' in i:
            miny = int(i[1])
            maxy = int(i[2])
        if 'Z' in i:
            minz = int(i[1])
            maxz = int(i[2])
    return (minx, maxx, miny, maxy, minz, maxz)

def threshold(heightmap, threshold):
    img = Image.open(heightmap)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i,j] >= (threshold, threshold, threshold):
                pixels[i,j] = (0, 0 ,0)

    img.show()
    img.save("thresholded_heightmap.png")

def normalize(z, Zmin, Zmax):
    return int((z - Zmin) / (Zmax - Zmin) * 255)

def get_normalized_average_Z(filepath):
    file = open(filepath, "r")
    file = file.read()
    file = file.split("\n")
    info = []
    for i in file:
        line = i.split(",")
        if len(line) > 1: info.append(line)

    Z = 0.0
    Zmin_local = float(info[0][2])
    Zmax_local = 0
    count = 0
    for i in info:
        if float(i[2]) > Zmax_local:
            Zmax_local = float(i[2])

        if float(i[2]) < Zmin_local:
            Zmin_local = float(i[2])

        Z += float(i[2])
        count += 1
    averageZ = Z/count
    normalizedZ = normalize(averageZ, Zmin_local, Zmax_local)

    #print("Zmin_local:",Zmin_local)
    #print("Zmax_local:",Zmax_local,"\n")

    #print("Average:",averageZ)
    #print("Normalized Average:",normalizedZ)

    return normalizedZ

def get_min_and_max_Z(filepath):
    file_list = os.listdir(filepath)
    Zmin_global = 1000000
    Zmax_global = 0
    
    for file in file_list:
        file = open(filepath+"/"+file, "r")
        file = file.read()
        file = file.split("\n")
        info = []
        for i in file:
            line = i.split(",")
            if len(line) > 1: info.append(line)

        Zmin_local = float(info[0][2])
        Zmax_local = 0
        count = 0
        for i in info:
            if float(i[2]) > Zmax_local:
                Zmax_local = float(i[2])

            if float(i[2]) < Zmin_local:
                Zmin_local = float(i[2])

        print(Zmin_local, Zmax_local)

        if Zmin_local < Zmin_global:
            Zmin_global = Zmax_local
        if Zmax_local > Zmax_global:
            Zmax_global = Zmax_local

    return (Zmin_global, Zmax_global)

def scale(Z, minimum, s):
    return (2**16 - 1) * ((Z - minimum)/s)

def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

def create_heightmap(point_cloud):
    '''
    # Extract information using LASHEADER 
    header_info = get_lasheader_info(point_cloud)

    # Get number of points and 
    # min and max x and y values 
    pc_num_points = count_points(header_info)
    boundaries = get_boundaries(header_info)
    print("Number of points:",pc_num_points)
    print("Boundaries:",boundaries)

    # Set height, width, Zmax, and Zmin based on boundaries
    Xmin = boundaries[0]
    Xmax = boundaries[1]
    Ymin = boundaries[2]
    Ymax = boundaries[3]
    Zmin = boundaries[4]
    Zmax = boundaries[5]
    
    H = Xmax - Xmin
    W = Ymax - Ymin
    r = 500
    print("\nXmin:",Xmin,"\nXmax:",Xmax,"\nYmin:",Ymin,"\nYmax:",Ymax,"\nZmin:",Zmin,"\nZmax:",Zmax)
    print("\nWidth:",W,"\nHeight:",H,)
    print("\nr:",r)

    image_W = int(W/r)
    image_H = int(H/r)
    print("\nImage_W:",image_W,"\nImage_H:",image_H,"\n")

    # Break point cloud into tiles
    if (not os.path.exists("./heightmap_tiles") and
        not os.path.exists("./heightmap_tiles_no_buffer")):
        print("RUNNING LASTILE")
        print(point_cloud)
        os.system("mkdir heightmap_tiles")
        os.system("mkdir heightmap_tiles_no_buffer")
        os.system("lastile -i " + point_cloud + " -tile_size 500 -buffer 50 -o heightmap_tiles/tile.las")
        print("DONE\n")
    '''

    # Get max and min height from tiles
    tile_height_min = 823.96
    tile_height_max = 2352.22
    if tile_height_min == 0 and tile_height_max == 0:
        tile_height_min, tile_height_max = get_min_and_max_Z("./heightmap_txt_tile_ground")
    #print("Absolute Min and Max:\n",tile_height_min,"\n",tile_height_max)
    #print("Normalized Min and Max:\n", normalize(tile_height_min, tile_height_min, tile_height_max), "\n", normalize(tile_height_max, tile_height_min, tile_height_max))

    scaling_factor = tile_height_max - tile_height_min
    #print("Scaling Factor:\n",scaling_factor)

    #print("Rescaled Min and Max:\n",scale(tile_height_min, tile_height_min, scaling_factor),"\n",scale(tile_height_max, tile_height_min, scaling_factor))

    
    # Call las2dem on each .las tile
    las2dem_command = "las2dem -i "
    
    tile_list = os.listdir("./heightmap_tiles_ground_(Copy)") #1013 total
    txt_tile_list = os.listdir("./heightmap_txt_tile_ground_(Copy)") #1013 total
    
    tile_range = 90

    for file in range(tile_range):
        # Update current Z values with scaled Z values
        with open("./heightmap_txt_tile_ground_(Copy)/"+str(txt_tile_list[file]), "rt") as fin:
            print("./heightmap_txt_tile_ground_(Copy)/"+str(txt_tile_list[file]))

            with open("./heightmap_txt_tile_ground_(Copy)/Rescaled_"+str(txt_tile_list[file]), "wt") as fout:
                print("./heightmap_txt_tile_ground_(Copy)/Rescaled_"+str(txt_tile_list[file]))

                for line in fin:
                    info = line.split(",")
                    print(info)
                    
                    currentZ = float(info[2])
                    print("Current:",currentZ)
                    normalizedZ = normalize(currentZ, tile_height_min, tile_height_max)
                    print("Normalized:",normalizedZ)
                    scaledZ = scale(currentZ, tile_height_min, scaling_factor)
                    print("Scaled:",scaledZ)

                    newline = line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n")
                    print(newline)

                    fout.write(line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n"))

        las2dem_command += "./heightmap_txt_tile_ground_(Copy)/Rescaled_"+str(txt_tile_list[file])+" "
        #if tile_list[file].endswith(".las"):
        #    las2dem_command += "./heightmap_tiles_ground_(Copy)/"+str(tile_list[file])+" "

    print("\nRUNNING LAS2DEM")
    las2dem_command += "-merged -elevation -o UAV_LIDAR_GROUND_HEIGHTMAP_FINAL.tif"
    os.system(las2dem_command)

    print("\nRUNNING GDAL_TRANSLATE")
    gdal_translate_command = "gdal_translate -of GTiff -ot Byte -scale 0 65535 0 255 UAV_LIDAR_GROUND_HEIGHTMAP_FINAL.tif UAV_LIDAR_GROUND_HEIGHTMAP_FINAL_RESCALED.tif"
    os.system(gdal_translate_command)