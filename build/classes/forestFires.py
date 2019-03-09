from scipy import spatial
from math import *
import pandas as pd
import numpy as np
from numpy import *

class forestFires():

    def __init__(self, fireDataFrame):

        if isinstance(fireDataFrame, pd.DataFrame):

            ## Process Data
            self.fireDataFrame = self.__cleanData(fireDataFrame)

            ## conversion to 3D catesian cordinants ##
            self.fireDataFrame['x'], self.fireDataFrame['y'], self.fireDataFrame['z'] = zip(
                *map(to_Cartesian, self.fireDataFrame['latitude'], self.fireDataFrame['longitude']))

            self.kdTreeFire = self.__generateKdTree(self.fireDataFrame)

        else:
            raise ValueError("incorrect data type: ")


    def __generateKdTree(self, dataFrame):

        if 'x' and 'y' and 'z' not in dataFrame.columns:
            raise ValueError("incorrect formatted dataFrame")

        else:
            coordinates = list(zip(dataFrame['x'], dataFrame['y'], dataFrame['z']))
            return spatial.KDTree(coordinates)

    def __cleanData(self, dataFrame, resetIndex=True):

        data = dataFrame.drop(['bright_ti4', 'scan', 'track', 'version', 'bright_ti5', 'frp', 'daynight'], axis=1)
        if (resetIndex == True):
            return data.reset_index()

        else:
            return data

    def getClosestAsset(self, x, y , z, bound):

        points = [x,y,z]
        ## test if variable exists##

        if (bound == None):
            return self.kdTreeFire.query(points, 1)
        else:
            return self.kdTreeFire.query(points, distance_upper_bound=bound)

    def getAssets(self, x, y, z, radius):

        points = zip(x, y, z)

        ## test if variable exists##
        if isinstance(self.kdTreeFire, spatial.KDTree):
            return self.kdTreeFire.query_ball_point(points, radius)

        else:
            return False

    def getDataFrame(self):
        return self.fireDataFrame

    def getTree(self):
        return self.kdTreeFire

def to_Cartesian(lat, lng):
    R = 6367 # radius of the Earth in kilometers

    lat = deg2rad(lat) ## conversion to radians
    lng = deg2rad(lng)  ## conversion to radians

    x = R * cos(lat) * cos(lng)
    y = R * cos(lat) * sin(lng)
    z = R * sin(lat)
    return x, y, z

def deg2rad(degree):

    rad = degree * 2*np.pi / 360
    return(rad)
