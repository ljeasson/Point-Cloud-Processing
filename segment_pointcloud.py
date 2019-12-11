import os
import glob

def process_tile(tileName):
    # Run LASNOISE to remove outlying points
    os.system("lasnoise -i " + tileName + ".las -remove_noise") # -ignore_class 2
    # Run LASGROUND to classify ground points
    os.system("lasground -i " + tileName + ".las")
    # Run LASHEIGHT to assign RGB values based on elevation 
    os.system("lasheight -i " + tileName +".las")
    # Run LASCLASSIFY to classify buildings and buildings and vegetation
    os.system("lasclassify -i " + tileName + ".las")

def segment_point_cloud(fileName):
    # Run LASTILE if not already pre-tiled
    if not os.path.exists("./tiles") and not os.path.exists("./tiles_no_buffer"): 
        print("RUNNING LASTILE")
        os.system("mkdir tiles")
        os.system("mkdir tiles_no_buffer")
        os.system("lastile -i " + fileName + ".las -tile_size 500 -buffer 50 -o ./tiles/tile.las")
        print("DONE\n")

    for tile in os.listdir("./tiles"):
        # Display tile name
        print("======================================")
        print("Processing",tile)

        # Get file name without ".las"
        tileName = "./tiles/" + tile[:tile.index(".")]

        # Process tile
        process_tile(tileName)
        
    #print("MERGING TILES")
    #os.system("lasmerge -i ./tiles/*.las -o " + fileName + "_merged.las")
    #print("DONE\n")

    # Run LASTILE to remove buffer
    print("REMOVING BUFFER")
    os.system("lastile -i tiles/tile_*.las -remove_buffer -odir tiles_no_buffer -olas")
    print("DONE\n")

    # Run LASSPLIT to split point clouds by classification
    print("RUNNING LASSPLIT")
    os.system("lassplit -i ./tiles_no_buffer/*.las -merged -o " + fileName + "_merged.las -by_classification")
    print("DONE\n")