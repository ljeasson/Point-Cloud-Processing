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
        if 'min' in i:
            minx = float(i[4])
            miny = float(i[5])
            minz = float(i[6])
        if 'max' in i:
            maxx = float(i[4])
            maxy = float(i[5])
            maxz = float(i[6])
        '''
        if 'X' in i:
            minx = int(i[1])
            maxx = int(i[2])
        if 'Y' in i:
            miny = int(i[1])
            maxy = int(i[2])
        if 'Z' in i:
            minz = int(i[1])
            maxz = int(i[2])
        '''
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

        #print(Zmin_local, Zmax_local)

        if Zmin_local < Zmin_global:
            Zmin_global = Zmax_local
        if Zmax_local > Zmax_global:
            Zmax_global = Zmax_local

    return (Zmin_global, Zmax_global)

def scale(Z, minimum, s):
    return (2**16 - 1) * ((Z - minimum)/s)

def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

def divide_chunks(l, n):   
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def create_heightmap(point_cloud, fileName):
    # Extract information using LASHEADER 
    header_info = get_lasheader_info(point_cloud)

    # Get min and max z values 
    #pc_num_points = count_points(header_info)
    boundaries = get_boundaries(header_info)
    print("Boundaries:",boundaries)

    # Set Zmax and Zmin based on boundaries
    Zmin = boundaries[4]
    Zmax = boundaries[5]
    scaling_factor = Zmax - Zmin
    print("\nZmin:",Zmin,"\nZmax:",Zmax,"\nScaling Factor:",scaling_factor)

    with open(str(fileName) + "_ground.txt", "rt") as fin:
        with open("RESCALED_" + str(fileName) + "_ground.txt", "wt") as fout:  
        
            for line in fin:
                info = line.split(",")
                    
                currentZ = float(info[2])
                scaledZ = scale(currentZ, Zmin, Zmax)

                newline = line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n")
                fout.write(line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n"))

    print("\nRUNNING BLAST2DEM")
    #os.system("dir/s/b RESCALED*.txt > ground_txt_tile_list.txt")
    #os.system("blast2dem -lof ground_txt_tile_list.txt -merged -elevation -o UAV_LIDAR_GROUND_HEIGHTMAP_FINAL_FROM_FILE.tif")
    os.system("blast2dem -i RESCALED_" + str(fileName) + "_ground.txt" + " -merged -elevation -o " + str(fileName) + "_NEW.tif")
    #os.system("blast2dem -i " + str(point_cloud) + " -merged -elevation -o " + str(fileName) + "_NEW.tif")
    print("DONE\n")

    print("RUNNING GDAL_TRANSLATE")
    gdal_translate_command = "gdal_translate -of GTiff -ot Byte -scale 0 65535 0 255 "+str(fileName)+"_NEW.tif "+str(fileName)+"_NEW_RESCALED.tif"
    os.system(gdal_translate_command)
    print("DONE")
    

    '''
    # Get max and min height from tiles
    print("\nGETTING MIN AND MAX Z-VALUES")
    tile_height_min = 823.96
    tile_height_max = 2352.22
    #tile_height_min, tile_height_max = 0,0
    if tile_height_min == 0 and tile_height_max == 0:
        tile_height_min, tile_height_max = get_min_and_max_Z("./heightmap_txt_tile_ground")
    
    scaling_factor = tile_height_max - tile_height_min
    
    print("\nRESCALING Z-VALUES")
    for file in range(tile_range):
        # Update current Z values with scaled Z values
        with open("./heightmap_txt_tile_ground/"+str(txt_tile_list[file]), "rt") as fin:
            with open("./heightmap_txt_tile_ground/Rescaled_"+str(txt_tile_list[file]), "wt") as fout:  
        
                for line in fin:
                    info = line.split(",")
                    
                    currentZ = float(info[2])
                    scaledZ = scale(currentZ, tile_height_min, scaling_factor)

                    newline = line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n")
                    fout.write(line.replace(line[find_2nd(line, ',')+1:], str("%.2f" % scaledZ)+"\n"))
    
        #las2dem_command += "./heightmap_txt_tile_ground/Rescaled_"+str(txt_tile_list[file])+" "

    print("\nRUNNING LAS2DEM")
    las2dem_command += "-merged -elevation -o UAV_LIDAR_GROUND_HEIGHTMAP_FINAL.tif"
    os.system(las2dem_command)
    #os.system("las2dem -i " + fileName + ".las -opng -keep_class 2 -hillshade -step 1 -nbits 16 -o " + fileName + "_heightmap.png")
    print("DONE\n")

    tile_list = os.listdir("./heightmap_tiles_ground") #1013 total
    txt_tile_list = os.listdir("./heightmap_txt_tile_ground") #1013 total
    txt_tile_list = sorted(txt_tile_list)
    
    tile_range = 60

    rescaled_txt_tile_list = []
    for tile in txt_tile_list:
        if "Rescaled_"  in tile:
            rescaled_txt_tile_list.append(tile)

    rescaled_txt_tile_list = list(divide_chunks(rescaled_txt_tile_list, tile_range))

    # Call blast2dem and gdal_translate on each .las txt tile
    raster_count = 0
    for i in rescaled_txt_tile_list:
        las2dem_command = "blast2dem -i "
        for tile in i:
            las2dem_command += "./heightmap_txt_tile_ground/"+str(tile)+" "
        
        print("\nRUNNING BLAST2DEM")
        las2dem_command += "-merged -elevation -o UAV_LIDAR_GROUND_HEIGHTMAP_FINAL"+str(raster_count)+".tif"
        os.system(las2dem_command)
        print("DONE")

        print("\nRUNNING GDAL_TRANSLATE")
        gdal_translate_command = "gdal_translate -of GTiff -ot Byte -scale 0 65535 0 255 UAV_LIDAR_GROUND_HEIGHTMAP_FINAL"+str(raster_count)+".tif UAV_LIDAR_GROUND_HEIGHTMAP_FINAL_RESCALED"+str(raster_count)+".tif"
        os.system(gdal_translate_command)
        print("DONE\n")

        raster_count += 1

        print("COMBINING RASTER TILES")
        os.system("dir /B *.tif > tif_tile_list.txt")
        os.system("gdalbuildvrt -input_file_list bil_list.txt mosaiced_image.vrt")
        os.system("gdal_translate -co COMPRESS=lzw mosaiced_image.vrt UAV_LIDAR_GROUND_HEIGHTMAP_RASTERIZED.tif")
        print("DONE\n")
    '''