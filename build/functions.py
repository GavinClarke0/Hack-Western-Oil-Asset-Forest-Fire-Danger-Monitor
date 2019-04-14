import numpy as np
import time
from math import *

def getMinDistance(lat1, long1, lat2, long2, min_distance):
    distance = getCordDistance(lat1, long1, lat2, long2)

    if (distance == np.nan or distance < min_distance):
        return distance
    else:
        return min_distance


def getCordDistance(lat1, long1, lat2, long2):
    # distance between two geographical locations

    t0 = time.time()

    lon1, lat1, lon2, lat2 = map(np.radians, [long1, lat1, long2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c

    t1 = time.time()

    return km

def to_Cartesian(lat, lng):
    R = 6367 # radius of the Earth in kilometers

    x = R * cos(lat) * cos(lng)
    y = R * cos(lat) * sin(lng)
    z = R * sin(lat)
    return x, y, z

def calcDangerLevel(distance, value):

    divisor = value/5

    if (distance > 4*divisor and distance <= value):
        return 5
    elif (distance > 3*divisor  and distance <= 4*divisor):
        return 4
    elif (distance >  2*divisor and distance <= 3*divisor):
        return 3
    elif (distance > divisor and distance <= 2*divisor):
        return 2
    else:
        return 1


def distToKM(x):
    R = 6367 # earth radius
    gamma = 2*np.arcsin(deg2rad(x/(2*R))) # compute the angle of the isosceles triangle
    dist = 2*R*sin(gamma/2) # compute the side of the triangle
    return(dist)

def deg2rad(degree):

    rad = degree * 2*np.pi / 360
    return(rad)

