import trimesh
import numpy as np

import pyrender


class SDF_Generator:
    
    def __init__(self, object_mesh_path, resolution, padding):

        self.resolution = resolution 
        self.padding = padding
        
        #loads mesh and centers the middle of the mesh on the origin 0,0,0
        self.mesh = trimesh.load(object_mesh_path)
        centering = trimesh.bounds.oriented_bounds(self.mesh, angle_digits=1, ordered=True, normal=None)
        self.mesh.apply_transform(centering[0])

    def get_sdf_array(self):
        #gets origin, dimension of sdf, the points and the spacing of the points 
        sdf_origin, sdf_dimensions = self.get_sdf_dimensions(self.padding)
        sdf_points, sdf_point_spacing = self.get_points(sdf_origin)

        #makes the sdf call on the points list and creates empty 3D array for final distances
        query = trimesh.proximity.ProximityQuery(self.mesh)
        distances = query.signed_distance(sdf_points)
        formatted_distances = np.zeros((self.resolution,self.resolution,self.resolution))

        #formats distances from 1D to 3D array as well as changing the sign
        count = 0 
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    formatted_distances[k][j][i] = -distances[count]
                    count+=1

        return formatted_distances, sdf_origin, sdf_point_spacing


    #returns origin point of the sdf as well as the dimensions of our sdf
    def get_sdf_dimensions(self, largest_dimension_padding):
       #find largest dimension of mesh and add padding
       mesh_extents = self.mesh.extents
       sdf_length = np.max(mesh_extents) + largest_dimension_padding*2
       #return the origin point of the sdf which will be in the bottom corner as well as our sdf dimensions
       sdf_origin = [-sdf_length/2, -sdf_length/2, -sdf_length/2]
       sdf_dimensions = [sdf_length, sdf_length, sdf_length]

       return sdf_origin, sdf_dimensions
       
    #returns list of points within the sdf cube space
    def get_points(self, sdf_origin):
        x = np.linspace(sdf_origin[0], abs(sdf_origin[0]), num=self.resolution, retstep=True)
        y = np.linspace(sdf_origin[1], abs(sdf_origin[1]), num=self.resolution, retstep=True)
        z = np.linspace(sdf_origin[1], abs(sdf_origin[1]), num=self.resolution, retstep=True)
        
        sdf_points = []
        sdf_point_spacing = x[1]
        
        #creates points from the linspace calculations
        for i in z[0]:
            for j in y[0]:
                for k in x[0]:
                    sdf_points.append([k,j,i])

        return sdf_points, sdf_point_spacing 
        
        


#if __name__ == "__main__":
#    test = SDF_Generator('123/objFiles/Measuring_Block_collision.obj', 32, .02) 
#    d, q, t = test.get_sdf_array()




#    mesh = trimesh.load('123/objFiles/Measuring_Block_collision.obj')
#centering = trimesh.bounds.oriented_bounds(mesh, angle_digits=1, ordered=True, normal=None)
#mesh.apply_transform(centering[0])
#print("info")
#print(centering[1])
#print(mesh.bounds)
#print(mesh.center_mass)
#print(mesh.extents)
#print(mesh.scale)
#print(mesh.units)

#sdf_origin, sdf_dimensions = get_sdf_dimensions(mesh.extents, .02)
#print(sdf_origin)
#print(sdf_dimensions)

#sdf_points, sdf_point_spacing = get_points(sdf_origin, 32)

    #d = get_sdf_array(sdf_points, mesh)
#    print(d[0][0][0])
#    print(d[16][0][16])
#    print(d[0][16][16])
#    print(d[1][2][3])
#print(trimesh.proximity.closest_point(mesh, [[-.06, -.06, -.06]]))
#    array = []
#
#    array.append([-.06,-.06,-.06])
#    array.append([.0019,-.06,.0019])
#    array.append([-.06,.0019,.0019])
#cloud = pyrender.Mesh.from_points(array)
#mesh.visual.face_colors = [100, 100, 100, 100]
#pointsss = trimesh.points.PointCloud(array)
#scene = trimesh.Scene([pointsss, mesh])
#(scene).show(smooth=False)
#
