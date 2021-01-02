# SDF-generator
Generates a signed distance field over the bounding box of a .obj mesh file using trimesh. Also allows you to save generated SDF's to pickle files, to perform trilinear interpolation of a given point and to vizualize final SDF.

Intended for use in hand simulator collision detections and distance querys. 

<img src="/images/box.png" width="400" height="400" style=display:inline-block/> <img src="/images/teapot.png" width="400" height="400"/>

### Dependencies:
Requires trimesh, libspatialindex, Rtree and pyrender for full functionality.
```
pip3 install trimesh
pip3 install pyrender
sudo apt install libspatialindex-dev
pip3 install Rtree
```

###


### TODO:

Change over to cpickle for better performance

Restructure class to make a little more sense with pickle additions and clean things up

Possibly change the way bounds are calculated need to test and see if weird behavior for strange meshes occur


