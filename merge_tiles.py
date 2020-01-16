import os
import glob
from multiprocessing import Process

def las2las_tile(directory,tile):
    las2las_tile_command = "las2las -i " + str(directory) + "\\" + str(tile) + " -set_version 1.4 -keep_random_fraction 0.1 -odir " + str(directory) + "\converted_subsampled"
    #print(las2las_tile_command)
    print("Process Start:", tile)
    os.system(las2las_tile_command)
    print("Process Done")

def merge_tiles(directory, subsample_factor):  
    filename = directory[directory.rfind("\\")+1 :]
    
    os.system("mkdir " + directory + "\converted_subsampled")
    os.system("mkdir " + directory + "\merged")

    print("RUNNING LAS2LAS ON TILES")
    processes = []
    for tile in os.listdir(directory):
        processes.append(Process(target=las2las_tile, args=(directory, tile,)))

    for p in processes: p.start()
    for p in processes: p.join()

    #las2las_command = "las2las -i " + str(directory) + "\*.laz -set_version 1.4 -keep_random_fraction 0.1 -odir " + str(directory) + "\converted_subsampled" 
    #print(las2las_command)
    #os.system(las2las_command)
    print("DONE\n")
    
    print("RUNNING LASMERGE")
    lasmerge_command = "lasmerge -i " + str(directory) + "\converted_subsampled\*.las -o " + str(directory) + "\merged\\" + str(filename) + "_merged.las"
    print(lasmerge_command)
    os.system(lasmerge_command)
    print("DONE\n")

    print("RUNNING LAS2LAS ON MERGED POINT CLOUD")
    las2las_command = "las2las -i " + str(directory) + "\merged\*.las -set_version 1.4 -keep_random_fraction " + str(subsample_factor) + " -o " + str(directory) + "\merged\\" + str(filename) + "_merged_subsampled.las" 
    print(las2las_command)
    os.system(las2las_command)
    print("DONE\n")