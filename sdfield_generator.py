import trimesh
import numpy as np
import pickle



class SDF_Generator:
    
    def __init__(self, object_mesh_path, resolution = 32, padding = .05, file_name = None):

        self.object_mesh_path = object_mesh_path
        
        #if file name is given then we load from pickle file
        if(file_name != None):
            sdf_file = open(file_name, "rb")
            sdf_properties = pickle.load(sdf_file)

            self.resolution = sdf_properties["resolution"]
            self.padding = sdf_properties["padding"]
            self.sdf_point_spacing = sdf_properties["sdf_point_spacing"]
            self.sdf_array = sdf_properties["sdf_array"]
            self.sdf_points = sdf_properties["sdf_points"]
            self.sdf_origin = sdf_properties["sdf_origin"]

        #otherwise initialize from parameters
        else: 
            self.resolution = resolution 
            self.padding = padding
            self.sdf_point_spacing = 0
            self.sdf_array = np.zeros((self.resolution,self.resolution,self.resolution))
            self.sdf_points = []
            self.sdf_origin = []

        #loads mesh and centers the middle of the mesh on the origin 0,0,0
        self.mesh = trimesh.load(object_mesh_path)
        centering = trimesh.bounds.oriented_bounds(self.mesh, angle_digits=1, ordered=True, normal=None)
        self.mesh.apply_transform(centering[0])

    #instead of recalculating just get properties
    def get_sdf_properties(self):
        return self.sdf_array, self.sdf_origin, self.sdf_point_spacing, self.resolution

    #calculates sdf and returns all the relevant properties
    def calculate_sdf_array(self):
        #gets origin, dimension of sdf, the points and the spacing of the points 
        self.sdf_origin, sdf_dimensions = self.get_sdf_dimensions(self.padding)
        self.sdf_points = self.get_points(self.sdf_origin)

        #makes the sdf call on the points list and creates empty 3D array for final distances
        query = trimesh.proximity.ProximityQuery(self.mesh)
        self.distances = query.signed_distance(self.sdf_points)

        #formats distances from 1D to 3D array as well as changing the sign
        count = 0 
        for i in range(self.resolution):
            for j in range(self.resolution):
                for k in range(self.resolution):
                    self.sdf_array[k][j][i] = -self.distances[count]
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
        

    #TODO change to cpickle for better performance
    def create_sdf_file(self, file_name): 
        #creates file
        sdf_file = open(file_name, "wb")

        #stores properties in dictionary
        sdf_properties = {} 
        sdf_properties["resolution"] = self.resolution
        sdf_properties["padding"] = self.padding
        sdf_properties["sdf_point_spacing"] = self.sdf_point_spacing
        sdf_properties["sdf_array"] = self.sdf_array
        sdf_properties["sdf_points"] = self.sdf_points
        sdf_properties["sdf_origin"] = self.sdf_origin

        #creates pickle file and closes it
        pickle.dump(sdf_properties, sdf_file)
        sdf_file.close()
        


    #uses trilinear interpolation to interpolate sdf value from given point
    def interpolate_sdf_from_point(self, given_point):
        x_given = given_point[0]
        y_given = given_point[1] 
        z_given = given_point[2] 

        #finding corresponding closest array index in sdf_array for given point
        x_sdf = int(abs(np.floor((x_given - self.sdf_origin[0]) / self.sdf_point_spacing)))
        y_sdf = int(abs(np.floor((y_given - self.sdf_origin[1]) / self.sdf_point_spacing)))
        z_sdf = int(abs(np.floor((z_given - self.sdf_origin[2]) / self.sdf_point_spacing)))
        
        #if outside the bounds of our sdf we return -1
        if x_sdf >= self.resolution-1 or y_sdf >= self.resolution-1 or z_sdf >= self.resolution-1:
            return -1
        if x_sdf <= 0 or y_sdf <= 0 or z_sdf <= 0:
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


    def visualize_sdf(self, mesh=False, user_points=None):

        #vizualizes user points if given
        if(user_points != None):
            user_point_colors = [[0,0,0,255]]*len(user_points)
            user_point_cloud = trimesh.points.PointCloud(user_points, user_point_colors)
        else:
            user_point_cloud = None


        #sets colors of all sdf points and turns them into a point cloud
        point_colors = [[102,178,255,100]]*len(self.sdf_points)

        #vizualizes mesh with sdf around it
        if(mesh == True):
            for i in range(len(self.sdf_points)):
                #sets up axis
                if(self.sdf_points[i][1] == self.sdf_origin[0] and self.sdf_points[i][2] == self.sdf_origin[0]):
                    point_colors[i] = [255,0,0,255]
                
                elif(self.sdf_points[i][0] == self.sdf_origin[0] and self.sdf_points[i][1] == self.sdf_origin[0]):
                    point_colors[i] = [0,0,255,255]
               
                elif(self.sdf_points[i][2] == self.sdf_origin[0] and self.sdf_points[i][0] == self.sdf_origin[0]):
                    point_colors[i] = [0,255,0,255]

            point_cloud = trimesh.points.PointCloud(self.sdf_points, point_colors)
            #self.mesh.visual.face_colors = [100, 100, 100, 100]
            scene = trimesh.Scene([point_cloud, self.mesh, user_point_cloud])

        #vizualizes sdf points only with respective colors
        else:
            
            for i in range(len(self.sdf_points)):

                #gets correct index for NXNXN array of sdf values from N array
                index_total = i
                z = min(self.resolution, i // self.resolution**2)
                index_total -= z * self.resolution**2
                y = min(self.resolution, index_total // self.resolution) 
                index_total -= y * self.resolution
                x = index_total // 1

                #vizualizes any points witihn object in red
                if(self.sdf_array[x][y][z] < 0 and self.sdf_array[x][y][z] != -1):
                    point_colors[i] = [255,0,0,255]

                #sets up axis
                elif(self.sdf_points[i][1] == self.sdf_origin[0] and self.sdf_points[i][2] == self.sdf_origin[0]):
                    point_colors[i] = [255,0,0,255]
                
                elif(self.sdf_points[i][0] == self.sdf_origin[0] and self.sdf_points[i][1] == self.sdf_origin[0]):
                    point_colors[i] = [0,0,255,255]
               
                elif(self.sdf_points[i][2] == self.sdf_origin[0] and self.sdf_points[i][0] == self.sdf_origin[0]):
                    point_colors[i] = [0,255,0,255]

            point_cloud = trimesh.points.PointCloud(self.sdf_points, point_colors)
            scene = trimesh.Scene([point_cloud, user_point_cloud])

        #renders scene
        (scene).show(smooth=False)

