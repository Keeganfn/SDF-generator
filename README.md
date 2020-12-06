# SDF-generator
Generates a signed distance field over the volume of a cube for a .obj mesh file using trimesh. Intended for use in the hand simulator collisions and distance querys. Also provides a trilinear interpolation function for a given point.


TODO:
Currently is set up as a class, need to add the ability to save the 3d SDF array to a file and a command line interface. Also need to adjust the way the extents are found as it could be an issue for irregular objects.
