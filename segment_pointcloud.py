import os
import glob
import multiprocessing

'''
def process_tile(tileName):
    # Run LASNOISE to remove outlying points
    os.system("lasnoise -i " + tileName + ".las -remove_noise") # -ignore_class 2
    # Run LASGROUND to classify ground points
    os.system("lasground -i " + tileName + ".las")
    # Run LASHEIGHT to assign RGB values based on elevation 
    os.system("lasheight -i " + tileName +".las")
    # Run LASCLASSIFY to classify buildings and buildings and vegetation
    os.system("lasclassify -i " + tileName + ".las")
'''

def segment_point_cloud(pointCloud, fileName):
    if not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject.txt"): 
        print("RUNNING LAS2TXT")
        las2txt_command = "las2txt -i " + str(pointCloud) + " -o " + str(fileName) + ".txt -parse xyzic -sep comma"
        os.system(las2txt_command)
        print("DONE\n")

    if not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_ground.txt") and \
       not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_vegetation.txt"): 
        print("POPULATE GROUND AND VEG TXT FILES")
        with open(str(fileName) + ".txt", "rt") as fin:
            with open(str(fileName) + "_ground.txt", "wt") as fout_G:
                with open(str(fileName) + "_vegetation.txt", "wt") as fout_V: 
                    for line in fin:
                        line_split = line.split(',')
                        if line_split[4] == '4\n':
                            fout_V.write(line)
                        if line_split[4] == '2\n':
                            fout_G.write(line)
        print("DONE\n")

    if not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_vegetation_no_noise.las"):
        print("RUNNING TXT2LAS AND LASNOISE FOR VEGETATION")
        os.system("txt2las -i " + str(fileName) + "_vegetation.txt -o " + str(fileName) + "_vegetation.las -parse xyzic")
        os.system("lasnoise -i " + str(fileName) + "_vegetation.las -o "+ str(fileName) + "_vegetation_no_noise.las -remove_noise -ignore_class 2")
        print("DONE\n")

    if not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_ground_no_noise.las"):
        print("RUNNING TXT2LAS FOR GROUND")
        os.system("txt2las -i " + str(fileName) + "_ground.txt -o " + str(fileName) + "_ground.las -parse xyzic")
        print("RUNNING LASNOISE FOR GROUND")
        os.system("lasnoise -i " + str(fileName) + "_ground.las -o "+ str(fileName) + "_ground_no_noise.las -remove_noise -ignore_class 2")

    if not os.path.exists("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_ground_no_noise_thinned.las"):
        print("RUNNING LAS2DEM FOR GROUND")
        os.system("las2dem -i " + str(fileName) + "_ground_no_noise.las -o "+ str(fileName) + "_ground_no_noise.laz -kill 500")
        print("RUNNING LASZIP FOR GROUND")
        os.system("laszip -i " + str(fileName) + "_ground_no_noise.laz")
        print("RUNNING LASTHIN FOR GROUND")
        os.system("lasthin -i " + str(fileName) + "_ground_no_noise.las -o " + str(fileName) + "_ground_no_noise_thinned.las -highest -step 2.0 -adaptive 0.2 5.0")
        print("RUNNING LAS2TXT FOR GROUND")
        os.system("las2txt -i " + str(fileName) + "_ground_no_noise_thinned.las -o " + str(fileName) + "_ground_no_noise_thinned.txt -parse xyzic -sep comma")
        print("DONE\n")

    
    '''
    # Run LASTILE if not already pre-tiled
    if not os.path.exists("./tiles"): 
        print("RUNNING LASTILE")
        os.system("mkdir tiles")
        
        os.system("lastile -i " + fileName + ".las -tile_size 500 -buffer 50 -o ./tiles/tile.las")
        print("DONE\n")

    if not os.path.exists("./tiles_no_buffer"):
        os.system("mkdir tiles_no_buffer")
        #p = []
        for tile in os.listdir("./tiles"):
            print("======================================")
            print("Processing",tile)

            # Get file name without ".las"
            tileName = "./tiles/" + tile[:tile.index(".")]

            # Process tile
            process_tile(tileName)
            #p1 = multiprocessing.Process(target=process_tile, args=(tileName, )) 
            #p.append(p1)
            
        # Multiprocessing on tiles
        for i in p: i.start()
        for i in p: i.join()

        # Run LASTILE to remove buffer
        print("REMOVING BUFFER")
        os.system("lastile -i tiles/tile_*.las -remove_buffer -odir tiles_no_buffer -olas")
        print("DONE\n")

    print("MERGING TILES")
    os.system("lasmerge -i ./tiles_no_buffer/*.las -o " + fileName + "_merged.las")
    print("DONE\n")

    #Run LAS2LAS with Ground (class 2) filter
    print("RUNNING LAS2LAS, Ground")
    os.system("las2las -i " + fileName + "_merged.las -drop_class 4 -o " + fileName + "_ground.las")
    print("DONE\n")
    #Run LAS2LAS with Vegetation (class 4) filter
    print("RUNNING LAS2LAS, Vegetation")
    os.system("las2las -i " + fileName + "_merged.las -drop_class 2 -o " + fileName + "_vegetation.las")
    print("DONE\n")


    # Run LASSPLIT to split point clouds by classification
    print("RUNNING LASSPLIT")
    os.system("lassplit -i ./tiles_no_buffer/*.las -merged -o " + fileName + "_merged.las -by_classification")
    print("DONE\n")
    '''