# SDF-generator
Generates a signed distance field over the bounding box of a .obj mesh file using trimesh. Also allows you to save generated SDF's to pickle files, to perform trilinear interpolation of a given point and to vizualize final SDF.

Intended for use in hand simulator collision detections and distance querys. 

<img src="/images/box.png" width="400" height="400" style=display:inline-block/> <img src="/images/teapot.png" width="400" height="400"/>

## Dependencies:
Requires trimesh, libspatialindex, Rtree and pyrender for full functionality.
```
pip3 install trimesh
pip3 install pyrender
sudo apt install libspatialindex-dev
pip3 install Rtree
```

## Usage:
#### Generate an SDF
* Look at the commented example.py to get a feel for basic functionality like generating the SDF, saving to a pickle file, loading from a pickle file, vizualization and interpolation.

#### Use the built in script to generate an SDF pickle file
* Use create_new_sdfield.py to generate/vizualize an SDF using command line with the format:
```
./create_new_sdfield.py 'Path to obj mesh' Resolution Padding 'Pickle file name with .pickle extension'
EX: ./demo_sdf.py 'obj_mesh/Measuring_Block.obj' 32 .02 'test.pickle'
```
* Dont go too much over 32 for resolution or under .02 for padding as it can get very slow or in the case of padding not work properly in some cases.

#### Vizualizing
* You can vizualize the created SDF with the vizualize function, you can use this to check if it was created correctly, you can also display user defined points and display the original mesh by setting the flags. Shown below.

<img src="/images/torus.png" width="400" height="400" style=display:inline-block/> <img src="/images/torus_mesh.png" width="400" height="400"/>



## TODO:

Change over to cpickle for better performance

Restructure class to make a little more sense with pickle additions and clean things up

Possibly change the way bounds are calculated need to test and see if weird behavior for strange meshes occur

Add better documentation

Optimize for complex meshes


