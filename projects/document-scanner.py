import cv2
import numpy as np
from utils import stackImages

# ----------------------------------------
# ----------- DOCUMENT SCANNER -----------
# ----------------------------------------
# Makes papers to look like scanned and fixes distortion
# Steps to perform
# 1) Resize image to given width
# 2) Convert img to greyscale
# 3) Apply Gaussian blur
# Using a Gaussian Blur filter before edge detection aims to reduce the level of noise in the image,
# which improves the result of the following edge-detection algorithm
# 4) Find edges using Canny edge detection https://docs.opencv.org/master/da/d22/tutorial_py_canny.html
# 5) Add 2 dilations and 1 erosion to thicken edges
# 6) Find biggest contour (same-coloured area) that has 4 corners
# 7) Warp paper to fix potential distortion and get birds-eye view
#
# NOTE! with normal low quality web can this won't give very accurate results. with high quality webcam or
# applying same logic to a good quality image, results are much better than with low quality webcam

# SCANNER CONFIG
imgWidth = 640
imgHeight = 480
paperArea = 0

# WEBCAM SETUP
# Camera Id can be 0 or 1 depending on your machine
capture = cv2.VideoCapture(1)
capture.set(3, imgWidth)
capture.set(4, imgHeight )
capture.set(10, 150)

# prepares image edges to be white and rest of the image to be black
def preProcessing(img):
    # img to grayscale
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # blur image
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # detect edges by using canny
    imgCanny = cv2.Canny(imgBlur, 150, 150)
    # enhance edges by using dilation/erosion to thicken the edges and make sure all content is scanned
    kernel = np.ones((5, 5))
    # apply dilation 2 times
    imgDilated = cv2.dilate(imgCanny, kernel, iterations=2)
    # apply erosion 1 time
    imgThres = cv2.erode(imgDilated, kernel, iterations=1)
    return imgThres

# get area of same color (contour) from image
def getContours(img):
    biggestContourCornerPoints = np.array([])
    paperArea = 0
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        # too small areas not detected
        if area > 5000:
            perimeter = cv2.arcLength(contour, True)
            # get approximated number of corners based on contoour perimeter
            approximateCornerPoints = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            # scanned paper is assumed to be rectangle (4 corners)
            # it is assumed that biggest contour with 4 corners in the image is the paper
            if area > paperArea and len(approximateCornerPoints) == 4:
                # keep track of the biggestContourCornerPoints area from the loop
                biggestContourCornerPoints = approximateCornerPoints
                paperArea = area

    # display biggestContourCornerPoints same-colored area (paper)
    cornerPointSize = 20
    cornerPointColor = (255, 0, 0) # blue
    cv2.drawContours(imgContour, biggestContourCornerPoints, -1, cornerPointColor, cornerPointSize)
    return biggestContourCornerPoints

# new points for straightened image (warping)
def reorder (myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    #print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis = 1)
    myPointsNew[1]= myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    #print("NewPoints",myPointsNew)
    return myPointsNew

def getWarp(img, biggestContourCornerPoints):
    biggestContourCornerPoints = reorder(biggestContourCornerPoints)
    # based on the point values we can see which comes first
    pts1 = np.float32(biggestContourCornerPoints)
    pts2 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))
    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(imgWidth,imgHeight))

    return imgCropped

while True:
    success, img = capture.read()
    img = cv2.resize(img, (imgWidth, imgHeight))
    imgContour = img.copy()

    imgThres = preProcessing(img)
    biggestContourCornerPoints = getContours(imgThres)
    # warp image only if contours found
    if biggestContourCornerPoints.size != 0:
        imgWarped = getWarp(img, biggestContourCornerPoints)
        imageArray = ([img, imgThres], [imgContour, imgWarped])
        #imageArray = ([imgContour, imgWarped])
        # display warped (scanned) image in its own window
        print("Area of biggest contour: ")
        print(paperArea)
        cv2.imshow("ImageWarped", imgWarped)
    else:
        # display original image if contour not found
        imageArray = ([img, imgThres], [img, img])


    stackedImages = stackImages(0.6, imageArray)
    cv2.imshow("WorkFlow", stackedImages)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
