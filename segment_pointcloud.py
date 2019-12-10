import os
import glob

def process_tile(tileName):
    # Run LASNOISE to remove outlying points
    #print("RUNNING LASNOISE")
    os.system("lasnoise -i " + tileName + ".las -remove_noise -ignore_class 2")
    #print("DONE\n")

    # Run LASGROUND to classify ground points
    #print("RUNNING LASGROUND")
    os.system("lasground -i " + tileName + ".las")
    #print("DONE\n")

    # Run LASHEIGHT to assign RGB values based on elevation 
    #print("RUNNING LASHEIGHT")
    os.system("lasheight -i " + tileName +".las")
    #print("DONE\n")

    # Run LASCLASSIFY to classify buildings and buildings and vegetation
    #print("RUNNING LASCLASSIFY")
    os.system("lasclassify -i " + tileName + ".las")
    #print("DONE\n")

def process_point_cloud(fileName):
    # Run LASTILE if not already pre-tiled
    if not os.path.exists("./tiles") and not os.path.exists("./tiles_no_buffer"): 
        print("RUNNING LASTILE")
        os.system("mkdir tiles")
        os.system("mkdir tiles_no_buffer")
        os.system("lastile -i " + fileName + ".las -tile_size 500 -buffer 50 -o tiles/tile.las")
        print("DONE\n")

    for file in os.listdir("./tiles"):
        # Display full file name
        #print("======================================")
        #print("Processing",file)

        # Get file name without ".las"
        tileName = "./tiles/" + file[:file.index(".")]
        #print("File Name:",tileName,"\n")

        # Begin tile processing
        process_tile(tileName)

    # Run LASTILE to remove buffer
    #if os.path.exists("./tiles"): 
    #    os.system("rmdir tiles")
    #if os.path.exists("./tiles_no_buffer"): 
    #    os.system("rmdir tiles_no_buffer")
        
    #print("MERGING TILES")
    #os.system("lasmerge -i ./tiles/*.las -o " + fileName + "_merged.las")
    #print("DONE\n")

    print("REMOVING BUFFER")
    os.system("lastile -i tiles/tile_*.las -remove_buffer -odir tiles_no_buffer -olas")
    print("DONE\n")

    print("RUNNING LASSPLIT")
    os.system("lassplit -i ./tiles_no_buffer/*.las -merged -o " + fileName + "_merged.las -by_classification")
    print("DONE\n")

    print("CREATING HEIGHTMAP")
    os.system("las2dem -i " + fileName + ".las -opng -keep_class 2 -hillshade -step 1 -nbits 16 -o " + fileName + "_heightmap.png")
    print("DONE\n")