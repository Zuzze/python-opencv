import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



path = 'Resources/cars.jpg'

# --- COLOR DETECTION ---
# 1) convert image to HSV
# 2) We don't usually know the color range so to help find the color range visually we use trackbars
# 3) Use min and max values to filter particular color from image using a mask
# 4) Add color to mask to see only filtered color from images

# Important: Name must be same in all ("Trackbars")
# createTrackbar requires always a function so we define just empty
def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)

# NOTE:
# For HSV, hue range is [0,179],
# saturation range is [0,255],
# value range is [0,255].
# Different software use different scales so if you are comparing
# OpenCV values with them, you need to normalize these ranges.
# https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # use hue, saturation and value from trackbar window values
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    # HOW TO FIND HSV VALUES (COLOR) TO DETECT WITHOUT TRACKBAR
    # green = np.uint8([[[0, 255, 0]]])
    # hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    # print(hsv_green)
    # >> [[[60 255 255]]]
    # Now you take [H-10, 100,100] and [H+10, 255, 255] as the lower bound and upper bound respectively.
    # Apart from this method, you can use any image editing tools like GIMP or any online converters to find these values,
    # but don't forget to adjust the HSV ranges.

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_min,s_max,v_max])
    # use mask to detect a particular color in a given image using lower and upper limit
    # filter out image of given color
    # mask will return black and white image
    mask = cv2.inRange(imgHSV,lower,upper)
    # to display color we want to detect in black and white color, we can use bitwise_and
    # - gets colored original pixel from original image if mask has a white pixel
    # - if mask pixel is black, it will remain black
    imgResult = cv2.bitwise_and(img,img,mask=mask)


    # cv2.imshow("Original",img)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    # to display images more nicely, use stack to display original, HSV, masked img and final filtered result image with detected color
    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)

    cv2.waitKey(1)
