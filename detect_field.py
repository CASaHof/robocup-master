import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys


from src.CASENV import CASENV

# model = YOLO('./yolov8x.pt')  # load an official detection model
# Create a numpy array to store the selected points
points = np.zeros((0, 2))

matplotlib.use('TkAgg')

# https://stackoverflow.com/a/67686428
def order_points(points):
    pts = np.array(points)
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def parseData(data):
    print(data)
    f = open("field", "w")
    data = order_points(data)
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



width = 640.0
height = 480.0
capture = cv2.VideoCapture(CASENV.CAM_ID)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
ret, frame = capture.read()
time.sleep(1/3)


while(not points.any()):
    ret, frame = capture.read()
    drawGameArea(frame)
    # cv2.imshow(".",frame)
    # cv2.waitKey()
