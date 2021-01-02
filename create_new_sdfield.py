#!/usr/bin/env python3

import sdfield_generator
import sys

if __name__ == "__main__": 

    if(len(sys.argv) == 5):

        sdf = sdfield_generator.SDF_Generator(str(sys.argv[1]), resolution = int(sys.argv[2]), padding = float(sys.argv[3])) 
        distance_array, sdf_origin, sdf_spacing, sdf_resolution = sdf.calculate_sdf_array()
        sdf.create_sdf_file(sys.argv[4])


    #new_sdf = sdfield_generator.SDF_Generator("obj_mesh/Measuring_Block.obj", file_name = "test_file.pickle") 


        sdf.visualize_sdf()

    else:
        print("INCORRECT ARGUMENTS")
        print("Please format command line arguments as 'Path to obj mesh' Resolution Padding 'Pickle file name with .pickle extension'")
        print("EX: ./demo_sdf.py 'obj_mesh/Measuring_Block.obj' 32 .02 'test.pickle' ")
        print("I dont recommend going much higher on the resolution or much lower on the padding\n\n\n")



