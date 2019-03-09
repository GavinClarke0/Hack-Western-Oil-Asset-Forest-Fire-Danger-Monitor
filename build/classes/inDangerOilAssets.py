from build/functions import getCordDistance, getMinDistance, calcDangerLevel, to_Cartesian
import numpy as np
from scipy import spatial
from getData import getFireData, getOilAssetData
import pandas as pd
from OilAssets import *
from forestFires import *


class inDangerAssets:

    # finds and stores csv of "indanger" assets

    def __init__(self, oilAssetCSV, FireDataCSV):

        oilDataFrame = oilAssetCSV.reset_index(drop=True)
        fireDataFrame = FireDataCSV.reset_index(drop=True)

        oilDataFrame['x'], oilDataFrame['y'], oilDataFrame['z'] = zip(
            *map(to_Cartesian, oilDataFrame['Latitude'], oilDataFrame['Longitude']))

        fireDataFrame['x'], fireDataFrame['y'], fireDataFrame['z'] = zip(
            *map(to_Cartesian, fireDataFrame['latitude'], fireDataFrame['longitude']))

        ## create class objects that store data ##



        fireData = forestFires(fireDataFrame)
        oilData = oilAssetData(oilDataFrame)

        self.inDangerAssets = self.__generateDangerAssets(fireData, oilData.getDataFrame())

        self.toCsv("C:\\Users\Gavin Clarke\Documents\HackWestern2018\DangerAssetCSVs\IndangerAssetsJan.csv")

        fireDataFrame.to_csv("C:\\Users\Gavin Clarke\Documents\HackWestern2018\DangerAssetCSVs\\fireAssetsJan.csv")
        oilDataFrame.to_csv("C:\\Users\Gavin Clarke\Documents\HackWestern2018\DangerAssetCSVs\\oilAssetsJan.csv")



    def getAssetFrame(self):
        return self.inDangerAssets


    def __generateDangerAssets(self, dataTree, dataTable):

        inDangerAssetList = []

        for index, row in dataTable.iterrows():

            x = row['x']
            y = row['y']
            z = row['z']

            query = dataTree.getClosestAsset( x, y, z, None)
            distance = query[0]
            location = query[1]

            ##KmDistance = distToKM(distance)
            if distance < 50:

                dangerLevel = calcDangerLevel(distance)

                dict = {'id': row['Well_Name'], 'Latitude': row['Latitude'], 'Longitude': row['Longitude'],
                        'dangerLevel': dangerLevel, 'Distance':distance, 'nearest': location}

                inDangerAssetList.append(dict)

        return pd.DataFrame(inDangerAssetList)

    def toCsv(self, path ):
        self.inDangerAssets.to_csv(path)

def deg2rad(degree):

    rad = degree * 2*np.pi / 360
    return(rad)

def distToKM(x):
    R = 6367 # earth radius
    gamma = 2*np.arcsin(deg2rad(x/(2*R))) # compute the angle of the isosceles triangle
    dist = 2*R*sin(gamma/2) # compute the side of the triangle
    return(dist)

def test():
    test = inDangerAssets(getOilAssetData(), getFireData())

test()
