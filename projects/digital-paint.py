import cv2
import numpy as np

# -------------------------------
# -------- DIGITAL PAINT --------
# -------------------------------
# Project that detects color from a webcam and allows user to paint into the image
# User can use any colored object
# For best results, it is recommended to configure used colors


# SETUP WEB CAM
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

# PAINT CONFIG
penTipThickness = 10
penCursorSize = 15
canvasPoints = [] # in format[x , y , colorId ]

# DETECTED COLORS
# setup colors you want to detect
# min/max hue and saturation values
# these color values can be found using color-picker.py
# goal is to keep color in mask white and rest of the mask should be black
# NOTE! values will depend on your shade of color and lighting so your values are probably not exactly same
# to find exact values for your colors, use color-picker.py
orange = [5,107,0,19,255,255]
purple = [133,56,0,159,156,255]
green = [57,76,0,100,255,255]
yellow = [20, 120, 143, 33, 255, 255]
lightGreen = [32, 51, 0, 90, 255, 255]
blue = [69, 98, 37, 146, 255, 255]
# Select colors you want to detect from video
detectedColors = [yellow, lightGreen, blue]

# PAINT COLORS
yellowPenColor = [0, 255, 255]
greenPenColor = [0, 255, 0]
bluePenColor = [255, 0, 0]
orangePenColor = [51,153,255]
purplePenColor = [255,0,255]
# setup line colors you want to draw in b, g, r format
paintColors = [yellowPenColor, greenPenColor, bluePenColor]

def getColorPoints(img, detectedColors, paintColors):
    # convert color to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # start from first detected color (i=0) and increase i always when moving to next color
    colorIndex = 0
    newPoints = []
    for color in detectedColors:
        # set upper and lower limits and display detected color using mask
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)

        # set paint to be circles
        cv2.circle(imgResult,(x,y), penCursorSize, paintColors[colorIndex], cv2.FILLED)

        # do not add points if position has not changed
        if x != 0 and y != 0:
            newPoints.append([x, y, colorIndex])
        colorIndex += 1
        #cv2.imshow(str(color[0]),mask)

    return newPoints

# contour -> area that has same color
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for contour in contours:
        area = cv2.contourArea(contour)
        # ignore too small areas
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            # detect bounding box for of the contour (same-colored) area polygon
            x, y, w, h = cv2.boundingRect(approx)

    # get horizontal center point of the bounding box (pen tip)
    return x+w//2, y

# draws a circle on points that user has touched with detected color
def drawOnCanvas(canvasPoints, paintColors):
    for point in canvasPoints:
        # point in format [x, y, color]
        cv2.circle(imgResult, (point[0], point[1]), penTipThickness,  paintColors[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    if img is None:
        print("image not found, check web cam input config")
        break
    imgResult = img.copy()

    # CHECK TRACKED COLORS AND THEIR POINTS
    # detect tracked colors from image
    # if no detected colors, newPoints = []
    newPoints = getColorPoints(img, detectedColors, paintColors)

    # IF TRACKED COLORS DETECTED => DRAW COLOR PATH TO CANVAS
    # check if new points was detected
    if len(newPoints) != 0:
        for newPoint in newPoints:
            canvasPoints.append(newPoint)
    # draw points on canvas
    if len(canvasPoints) != 0:
        drawOnCanvas(canvasPoints, paintColors)

    # SHOW IMAGE
    cv2.imshow("Result", imgResult)

    # CLOSE APP
    # close app pressing q for quit
    # waitKey(0) will display the window infinitely
    # waitKey(1) will display a frame for 1 ms, after which display will be automatically closed
    # due to "while True", each frame is displayed 1ms infinitely
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("App closed by the user")
        break

    # CLEAR CANVAS
    # erase canvas pressing e for erase
    if cv2.waitKey(1) & 0xFF == ord('e'):
        canvasPoints = []
