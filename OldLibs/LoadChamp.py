# Loads Lake Champlain bathymetric readings.
# Need to convert x,y,depth readings to a surface...
# MinX = 420142, MinY = 115042
# rangeX = 34470, rangeY = 17390

import numpy as np

# Test CSV reader
champXYD = np.genfromtxt("VT_Lake_Champlain_Bathymetry.csv", delimiter=',', skip_header=1, usecols=(0, 1, 3))
champX = np.genfromtxt("VT_Lake_Champlain_Bathymetry.csv", delimiter=',', skip_header=1, usecols=(0))
champY = np.genfromtxt("VT_Lake_Champlain_Bathymetry.csv", delimiter=',', skip_header=1, usecols=(1))
champD = np.genfromtxt("VT_Lake_Champlain_Bathymetry.csv", delimiter=',', skip_header=1, usecols=(3))
print("champXY shape", champX.shape)
minX = np.min(champX)
minY = np.min(champY)
minD = np.min(champD)
maxX = np.max(champX)
maxY = np.max(champY)
maxD = np.max(champD)
print("champX", champX[0], " min", minX, " max", maxX, "range", maxX - minX)
print("champY", champY[0], " min", minY, " max", maxY, "range", maxY - minY)
print("champD", champD[0], " min", minD, " max", maxD, "range", maxD - minD)
champX = champX - minX
champY = champY - minY
np.column_stack((champX, champY, champD))
for ii in range(20):
    print("[", champX[ii], ",", champY[ii], "=", champD[ii])