import numpy as np



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

if __name__=="__main__":
    corners = [[100,100],[200,50],[50,200],[200,200]]

    corners_out = order_points(corners)
    top_left,top_right,bottom_right,bottom_left = corners_out

    from PIL import Image, ImageDraw
    image = Image.new('RGB', (300, 300))

    draw = ImageDraw.Draw(image)
    draw.line((top_left[0],top_left[1],top_right[0],top_right[1]), fill="#ffffff",width=2)
    draw.line((top_left[0],top_left[1],bottom_left[0],bottom_left[1]), fill="#ff0000",width=2)
    draw.line((top_right[0],top_right[1],bottom_right[0],bottom_right[1]), fill="#00ff00",width=2)
    draw.line((bottom_left[0],bottom_left[1],bottom_right[0],bottom_right[1]), fill="#0000ff",width=2)


    image.save("tests/corner/image.png")
    print(f"Done! See tests/corner/image.png\nCorners in: {corners}\nCorners out: {corners_out}")