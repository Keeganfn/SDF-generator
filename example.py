#!/usr/bin/env python3

import sdfield_generator
import sys

if __name__ == "__main__": 

    #basic usage for creating an sdf pickle file and vizualizing it dont go much over 32 or under .02 for the parameters
    sdf = sdfield_generator.SDF_Generator("obj_mesh/Measuring_Block.obj", resolution = 32, padding = .02) 
    #gets properties
    distance_array, sdf_origin, sdf_spacing, sdf_resolution = sdf.calculate_sdf_array()
    #interpolates signed distance from a given point 
    print("DEMO INTERPOLATED SIGNED DISTANCE: " + str(sdf.interpolate_sdf_from_point([.03,.03,.03]))) 
    #creates pickle file
    sdf.create_sdf_file("demo_sdf_files/box.pickle")
    #vizualizing
    sdf.visualize_sdf()

    #load sdf file enter in the mesh file and corresponding pickle file
    loaded_sdf = sdfield_generator.SDF_Generator("obj_mesh/torus.obj", file_name="demo_sdf_files/torus.pickle") 
    #gets properties like above but skips previously done calculation
    distance_array, sdf_origin, sdf_spacing, sdf_resolution = loaded_sdf.get_sdf_properties()
    #vizualizing
    loaded_sdf.visualize_sdf()
    
    #optional flags for vizualization of a list of points or with the original mesh
    #loaded_sdf.visualize_sdf(mesh=True, user_points=[[0,0,0]])
    




