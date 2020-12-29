import cv2
import numpy as np
from utils import stackImages

# --- SHAPE DETECTION ---
# Task: detect triangles, rectangles and circles in an image
# 1) convert image to gray scale
# 2) Add blur
# 3) Detect edges in image (Canny edge detection)
# 4) Find contours (continuous points with same color/intensity)


# CONTOURS
# contour is a curve joining all the continuous points (along the boundary), having same color or intensity.
# The contours are a useful tool for shape analysis and object detection and recognition.
def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        print(area)
        if area > 500:
            # draw blue rectangle border with thickness of 3 for each shape
            # -1 => draw all contours
            cv2.drawContours(imgContour, contour, -1, (255, 0, 0), 3)

            # curve length (=perimeter) will help approximate how many corners the shape has
            # A perimeter is a path that encompasses/surrounds a two-dimensional shape (in Finnish: "Piiri")
            perimeter = cv2.arcLength(contour, True)
            #print(peri)
            # 0.02: experiment with this value
            # True: we are expecting all shapes too be closed
            # use approxPolyDP to get approximate corner points
            approximateCornerPoints = cv2.approxPolyDP(contour, 0.02 * perimeter,True)
            print(len(approximateCornerPoints))
            objectCorners = len(approximateCornerPoints)

            # BOUNDING BOX
            # add bounding box for detected shape
            x, y, w, h = cv2.boundingRect(approximateCornerPoints)
            ratioThreshold = 0.1
            squareMinRatio = 1 - ratioThreshold
            squareMaxRatio = 1 + ratioThreshold

            if objectCorners == 3:
                objectType = "Triangle"
            elif objectCorners == 4:
                # if width/height is close to 1 => square
                aspRatio = w/float(h)
                # print(aspRatio)
                if aspRatio > squareMinRatio and aspRatio < squareMaxRatio:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objectCorners > 4:
                # here we simplify that if object type is > 4 => circle
                objectType = "Circle"
            else:
                objectType = "None"


            # draw green line rectangle on top of image
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            # add shape name to image little bit (10px) left and higher of the center of the object
            textStartPoint = (x+(w//2)-50,
                         y+(h//2)-55)
            fontColor = (200,200,200)
            fontScale = 0.5
            fontWeight = 1
            cv2.putText(imgContour,
                        objectType,
                        textStartPoint,
                        cv2.FONT_HERSHEY_COMPLEX,
                        fontScale,
                        fontColor,
                        fontWeight
            )




path = 'Resources/shapes.jpg'
img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
getContours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8,([img,imgGray,imgBlur],
                            [imgCanny,imgContour,imgBlank]))
cv2.imshow("Stack", imgStack)
cv2.waitKey(0)