from scipy import spatial
import pandas as pd
import numpy as np


class oilAssetData():

    def __init__(self, oilDataFrame):

        if isinstance(oilDataFrame, pd.DataFrame):

            self.oilDataFrame = oilDataFrame

            ## conversion to 3D catesian cordinants ##
            self.oilDataFrame['x'], self.oilDataFrame['y'], self.oilDataFrame['z'] = zip(
                *map(to_Cartesian, self.oilDataFrame['Latitude'], self.oilDataFrame['Longitude']))

            self.kdTreeOilAsset = self.__generateKdTree(self.oilDataFrame)

        else:
            raise ValueError("incorrect data type: ")

    def __generateKdTree(self, dataFrame):


        if 'x' and 'y' and 'z' not in dataFrame.columns:
            raise ValueError("incorrect formatted dataFrame")

        else:

            coordinates = list(zip(self.oilDataFrame['x'], self.oilDataFrame['y'], self.oilDataFrame['z']))
            return spatial.KDTree(coordinates)

    def getClosestAsset(self, x, y ,z, bound = None):

        points = [x,y,z]

        ## test if variable exists##
        if isinstance(self.kdTreeOilAsset, spatial.KDTree):

            if bound == None:
                return self.kdTreeOilAsset.query(points)
            else:
                return self.kdTreeOilAsset.query(points, distance_upper_bound=bound)

    def getAssets(self, x, y, z, radius):

        points = zip(x, y, z)

        ## test if variable exists##
        if isinstance(self.kdTreeOilAsset, spatial.KDTree):
            return self.kdTreeOilAsset.query_ball_point(points, radius)

        else:
            return False
    def getDataFrame(self):
        return self.oilDataFrame



def to_Cartesian(lat, lon, R = 6371):
    """
    calculates lon, lat coordinates of a point on a sphere with
    radius R
    """
    lon_r = np.radians(lon)
    lat_r = np.radians(lat)

    x =  R * np.cos(lat_r) * np.cos(lon_r)
    y = R * np.cos(lat_r) * np.sin(lon_r)
    z = R * np.sin(lat_r)
    return x,y,z



def deg2rad(degree):

    rad = degree * 2*np.pi / 360
    return(rad)
