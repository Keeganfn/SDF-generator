import trimesh
import numpy as np
from scipy.interpolate import RegularGridInterpolator

import pyrender


class SDF_Generator:
    
    def __init__(self, object_mesh_path, resolution, padding):

        self.resolution = resolution 
        self.padding = padding
        self.sdf_point_spacing = 0
        self.sdf_array = np.zeros((self.resolution,self.resolution,self.resolution))
        self.sdf_origin = []

        #loads mesh and centers the middle of the mesh on the origin 0,0,0
        self.mesh = trimesh.load(object_mesh_path)
        centering = trimesh.bounds.oriented_bounds(self.mesh, angle_digits=1, ordered=True, normal=None)
        self.mesh.apply_transform(centering[0])

    def get_sdf_array(self):
        #gets origin, dimension of sdf, the points and the spacing of the points 
        self.sdf_origin, sdf_dimensions = self.get_sdf_dimensions(self.padding)
        sdf_points = self.get_points(self.sdf_origin)

        #makes the sdf call on the points list and creates empty 3D array for final distances
        query = trimesh.proximity.ProximityQuery(self.mesh)
        distances = query.signed_distance(sdf_points)

        #formats distances from 1D to 3D array as well as changing the sign
        count = 0 
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    self.sdf_array[k][j][i] = -distances[count]
                    count+=1

        return self.sdf_array, self.sdf_origin, self.sdf_point_spacing, self.resolution


    #returns origin point of the sdf as well as the dimensions of our sdf
    def get_sdf_dimensions(self, largest_dimension_padding):

       #find largest dimension of mesh and add padding
       mesh_extents = self.mesh.extents
       sdf_length = np.max(mesh_extents) + largest_dimension_padding*2
       #return the origin point of the sdf which will be in the bottom corner as well as our sdf dimensions
       sdf_origin = [-sdf_length/2, -sdf_length/2, -sdf_length/2]
       sdf_dimensions = [sdf_length, sdf_length, sdf_length]
       print(self.mesh.bounds)

       return sdf_origin, sdf_dimensions
       
    #returns list of points within the sdf cube space
    def get_points(self, sdf_origin):
        x = np.linspace(sdf_origin[0], abs(sdf_origin[0]), num=self.resolution, retstep=True)
        y = np.linspace(sdf_origin[1], abs(sdf_origin[1]), num=self.resolution, retstep=True)
        z = np.linspace(sdf_origin[1], abs(sdf_origin[1]), num=self.resolution, retstep=True)
        
        sdf_points = []
        self.sdf_point_spacing = x[1]

        #creates points from the linspace calculations
        for i in z[0]:
            for j in y[0]:
                for k in x[0]:
                    sdf_points.append([k,j,i])

        return sdf_points
        
    #uses trilinear interpolation to interpolate sdf value from given point
    def get_closest_sdf_points(self, given_point):
        x_given = given_point[0]
        y_given = given_point[1] 
        z_given = given_point[2] 

        #finding corresponding closest array index in sdf_array for given point
        x_sdf = int(abs(np.floor((x_given - self.sdf_origin[0]) / self.sdf_point_spacing)))
        y_sdf = int(abs(np.floor((y_given - self.sdf_origin[1]) / self.sdf_point_spacing)))
        z_sdf = int(abs(np.floor((z_given - self.sdf_origin[2]) / self.sdf_point_spacing)))
        
        #if outside the bounds of our sdf we return -1
        if x_sdf >= self.resolution or y_sdf >= self.resolution or y_sdf >= self.resolution:
            return -1

        #used equation and format from wikipedia article on trilinear interpolation if you wish to look at the math
        x_distance = (x_given - (x_sdf*self.sdf_point_spacing + self.sdf_origin[0])) / (((x_sdf+1)*self.sdf_point_spacing + self.sdf_origin[0]) - (x_sdf*self.sdf_point_spacing + self.sdf_origin[0]))
        y_distance = (y_given - (y_sdf*self.sdf_point_spacing + self.sdf_origin[1])) / (((y_sdf+1)*self.sdf_point_spacing + self.sdf_origin[1]) - (y_sdf*self.sdf_point_spacing + self.sdf_origin[1]))
        z_distance = (z_given - (z_sdf*self.sdf_point_spacing + self.sdf_origin[2])) / (((z_sdf+1)*self.sdf_point_spacing + self.sdf_origin[2]) - (z_sdf*self.sdf_point_spacing + self.sdf_origin[2]))

        #finds 8 surrounding values
        C000 = self.sdf_array[x_sdf][y_sdf][z_sdf]
        C100 = self.sdf_array[x_sdf+1][y_sdf][z_sdf]
        C010 = self.sdf_array[x_sdf][y_sdf+1][z_sdf]
        C001 = self.sdf_array[x_sdf][y_sdf][z_sdf+1]
        C101 = self.sdf_array[x_sdf+1][y_sdf][z_sdf+1]
        C110 = self.sdf_array[x_sdf+1][y_sdf+1][z_sdf]
        C011 = self.sdf_array[x_sdf][y_sdf+1][z_sdf+1]
        C111 = self.sdf_array[x_sdf+1][y_sdf+1][z_sdf+1]

        #interpolation steps
        C00 = C000*(1-x_distance) + (C100 * x_distance)
        C01 = C001*(1-x_distance) + (C101 * x_distance)
        C10 = C010*(1-x_distance) + (C110 * x_distance)
        C11 = C011*(1-x_distance) + (C111 * x_distance)

        C0 = C00*(1-y_distance) + (C10 * y_distance)
        C1 = C01*(1-y_distance) + (C11 * y_distance)

        C = C0*(1-z_distance) + (C1 * z_distance)

        return C


