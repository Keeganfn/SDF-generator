#!/usr/bin/env python3
import sdfield_generator


sdf = sdfield_generator.SDF_Generator("obj_mesh/Measuring_Block.obj", resolution = 32, padding = .02) 
distance_array, sdf_origin, sdf_spacing, sdf_resolution = sdf.calculate_sdf_array()

value = sdf.interpolate_sdf_from_point([0,0,0])
print(value)

sdf.create_sdf_file("test_file.pickle")

print("creating file")

new_sdf = sdfield_generator.SDF_Generator("obj_mesh/Measuring_Block.obj", file_name = "test_file.pickle") 
distance_array, sdf_origin, sdf_spacing, sdf_resolution = sdf.get_sdf_properties()


new_sdf.visualize_sdf()

