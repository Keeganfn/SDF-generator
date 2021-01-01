# SDF-generator
Generates a signed distance field over the volume of a cube for a .obj mesh file using trimesh. Intended for use in the hand simulator collisions and distance querys. Also provides a trilinear interpolation function for a given point.


TODO:
Command line tool
Fix loaded Pickle files not being able to be vizualized
Change over to cpickle for better performance
Documentation


MAYBE:
Restructure class to make a little more sense with pickle additions and clean things up
Possibly change the way bounds are calculated need to test and see if weird behavior for strange meshes occur
