# SDF-generator
Generates a signed distance field over the volume of a cube for a .obj mesh file using trimesh. Intended for use in the hand simulator collisions and distance querys.


TODO:
Currently is set up as a class, need to add the ability to save the 3d SDF array to a file and a command line interface. Also need to clean it up and adjust certain return values and the way the cube is centerd on the object. Would also be nice to have trilinear interpolation function built in for any arbitrary point.
