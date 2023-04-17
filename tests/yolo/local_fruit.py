from ultralytics import YOLO
from yt_dlp import YoutubeDL
from os.path import exists
import time
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

model = YOLO('./best.pt')  # load an official detection model

# https://im-coder.com/wie-berechne-ich-den-schnittpunkt-zweier-linien-in-python.html
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

width = 640
height = 480

top_left = (125,175)
top_right = (width-140,175)
bottom_left = (-30,height-120)
bottom_right = (width+5,height-120)

results = model(source=2, stream=True,verbose=False) 
for result in results:
    # print(result.orig_img)
    boxes = result.boxes  # Boxes object for bbox outputs
    im = Image.fromarray(result.orig_img[...,::-1].copy())
    img1 = ImageDraw.Draw(im)
    # im.save("test_raw.jpeg")

    img1.line([top_left,top_right], width=5, fill="#ffffff")
    img1.line([top_left,bottom_left], width=5, fill="#ffffff")
    img1.line([top_right,bottom_right], width=5, fill="#ffffff")
    img1.line([bottom_left,bottom_right], width=5, fill="#ffffff")
    for idx,c in enumerate(result.boxes.cls):
        # print(result.names[int(c)])
        # if result.names[int(c)]=="apple":
            # print(f"c={c} ({result.names[int(c)]}) {boxes.xyxy[idx]}")
            w, h = 220, 190
            shape = [(boxes.xyxy[idx][0], boxes.xyxy[idx][1]), (boxes.xyxy[idx][2],boxes.xyxy[idx][3])]
            position_x = boxes.xyxy[idx][0] + ((boxes.xyxy[idx][2] - boxes.xyxy[idx][0]) / 2)
            position_y = boxes.xyxy[idx][3]
            left_intersection = line_intersection((top_left,bottom_left),((0,position_y),(position_x,position_y)))
            right_intersection = line_intersection((top_right,bottom_right),((width,position_y),(position_x,position_y)))
            bottom_intersection = line_intersection((bottom_left,bottom_right),((position_x,position_y),(position_x,bottom_left[1])))
            top_intersection = line_intersection((top_left,top_right),((position_x,position_y),(position_x,top_left[1])))
            
            if left_intersection:
                img1.rectangle([
                    (left_intersection[0],position_y-1),
                    (position_x+1,position_y+1)
                ], fill ="blue")
            else:
                img1.rectangle([
                    (0,position_y-1),
                    (position_x+1,position_y+1)
                ], fill ="blue")

            if bottom_intersection:
                img1.rectangle([
                    (position_x,position_y),
                    (position_x+1,bottom_intersection[1]+1)
                ], fill ="blue")
            else:
                img1.rectangle([
                    (position_x,position_y),
                    (position_x+1,height)
                ], fill ="blue")
            
            if left_intersection and bottom_intersection and right_intersection and top_intersection:
                x_percent = int(((position_x - left_intersection[0]) / (right_intersection[0] - left_intersection[0])) * 100)/100
                y_percent = int(((position_y - bottom_intersection[1]) / (top_intersection[1] - bottom_intersection[1])) * 100)/100
                outline = "red"
                if x_percent>0 and x_percent<1 and y_percent>0 and y_percent<1:
                    outline = "green"
                img1.rectangle(shape, outline = outline, width=5)
                # y_percent = ((right_intersection[0] - left_intersection[0]))
                # print(f"x = {x_percent} | y = {y_percent}")
                # img1.text((position_x,position_y), fill ="white", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
                img1.text((position_x,boxes.xyxy[idx][1]-20), fill ="white", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")

    # fig, ax = plt.subplots()
    # ax.imshow(im)
    # ax.set_xlim([0, width])
    # ax.set_ylim([height, 0])
    # # cid = fig.canvas.mpl_connect('button_press_event', onclick)
    # plt.show()

    im.save("test.jpeg")


