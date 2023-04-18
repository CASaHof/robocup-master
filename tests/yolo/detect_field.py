from ultralytics import YOLO#

from yt_dlp import YoutubeDL
from os.path import exists
import time
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import tkinter
import sys

model = YOLO('./yolov8x.pt')  # load an official detection model
# Create a numpy array to store the selected points
points = np.zeros((0, 2))

matplotlib.use('TkAgg')

def parseData(data):
    print(data)
    f = open("field", "w")
    f.write(f"{data[0][0]}x{data[0][1]}\n")
    f.write(f"{data[1][0]}x{data[1][1]}\n")
    f.write(f"{data[2][0]}x{data[2][1]}\n")
    f.write(f"{data[3][0]}x{data[3][1]}\n")
    f.close()

def drawGameArea(img):
    # Open the image
    # img = Image.open('image.jpg')
    width, height = 640,480

    # Create a numpy array to store the selected points

    # Define the event handler for mouse clicks
    def onclick(event):
        global points
        # Ignore clicks outside of the image
        if event.xdata is None or event.ydata is None:
            return
        # Append the selected point to the array
        points = np.vstack((points, [int(event.xdata), int(event.ydata)]))
        if len(points) == 4:
            parseData(points)
            sys.exit()
        # Update the plot with the selected point
        plt.scatter(event.xdata, event.ydata, c='r')
        plt.draw()

    # Display the image and wait for the user to select points
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_xlim([0, width])
    ax.set_ylim([height, 0])
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

results = model(source=2, stream=True,verbose=False) 
t = True
for result in results:
    # if(not points.any()):
    if t:
        drawGameArea(result.orig_img)
        t = False