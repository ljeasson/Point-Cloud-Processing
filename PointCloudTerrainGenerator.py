import numpy as np
import matplotlib.pyplot as plt
import cv2

# Read data from text file
a = open("USCAYF20180722f1a1_180722_181152_1_dem_filter_reproject_ground.txt", "r")
a = a.read()
a = a.split("\n")
data = []
x = []
y = []
heights = []
intensity = []
for i in a:
    line = i.split(",")
    if len(line) > 1: 
        data.append(line)
        x.append(float(line[0]))
        y.append(float(line[1]))
        heights.append(float(line[2]))
        intensity.append(float(line[3]))

# Set precision
precision = 0.0625

# Set height values
minH = min(heights)
maxH = max(heights)
sizeH = len(heights)
rangeH = maxH - minH
for i in range(sizeH):
    heights[i] = round(heights[i] - minH, 2)

# Set intensity values
minInt = min(intensity)
maxInt = max(intensity)

# Set x,y coordinates with precision level
minX = min(x)
minY = min(y)
xInd = []
yInd = []
for i in range(sizeH):
    xInd.append((x[i]-minX) * precision)
    yInd.append((y[i]-minY) * precision)

# Initialize images
imgl = np.zeros([int(max(xInd)+1), int(max(yInd)+1)], dtype=int)
imgm = np.zeros([int(max(xInd)+1), int(max(yInd)+1)], dtype=int)
texture = np.zeros([int(max(xInd)+1), int(max(yInd)+1)], dtype=int)
imgl = imgl + 2 * maxH
imgnorm = np.zeros([int(max(xInd)+1), int(max(yInd)+1)], dtype=int)

'''
# Produce images
for i in range(sizeH):
    x1 = xInd[i] + 1
    y1 = yInd[i] + 1
    texture[x1][y1] = intensity[i]/maxInt
    
    if imgl[x1][y1] < heights[i]:
        imgl[x1][y1] < heights[i]
    
    if imgm[x1][y1] < heights[i]:
        imgm[x1][y1] < heights[i]
    
# Max correction
'''

