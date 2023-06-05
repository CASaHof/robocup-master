
import math
import time
import cv2
from matplotlib import pyplot as plt
import numpy as np


def loadData():
    # global top_left
    # global top_right
    # global bottom_right
    # global bottom_left
    width = 640
    height = 480
    f = open("field", "r")
    data = f.read().splitlines()
    top_left = (int(data[0].split("x")[0].split(".")[0]),int(data[0].split("x")[1].split('.')[0]))
    top_right = (int(data[1].split("x")[0].split(".")[0]),int(data[1].split("x")[1].split('.')[0]))
    bottom_right = (int(data[2].split("x")[0].split(".")[0]),int(data[2].split("x")[1].split('.')[0]))
    bottom_left = (int(data[3].split("x")[0].split(".")[0]),int(data[3].split("x")[1].split('.')[0]))
    bottom_center = (int(data[4].split("x")[0].split(".")[0]),int(data[4].split("x")[1].split('.')[0]))
    center = (int(data[5].split("x")[0].split(".")[0]),int(data[5].split("x")[1].split('.')[0]))
    top_center = (int(data[6].split("x")[0].split(".")[0]),int(data[6].split("x")[1].split('.')[0]))
    return top_left, top_right, bottom_right, bottom_left,width,height,bottom_center,center,top_center
    # print(data)
    
top_left, top_right, bottom_right, bottom_left,width,height,bottom_center,center,top_center = loadData()
top = (top_left[1]+top_right[1])/2
bottom = (bottom_left[1]+bottom_right[1])/2
# s = [top_left, top_right, bottom_right, bottom_left]
# print(top_left, top_right, bottom_right, bottom_left,width,height,middle_left)
print(f"top={top} center={center} bottom={bottom}")

x = np.array([top_center[0],top_center[0],center[0],bottom_center[0],bottom_center[0]])
y = np.array([top,top_center[1],center[1],bottom_center[1],bottom])

# calculate polynomial
z = np.polyfit(x, y, 5)
f = np.poly1d(z)

# calculate new x's and y's
# x_new = np.linspace(x[0], x[-1], 50)
# y_new = f(x_new)
print(f(100))
