import cv2
import numpy as np

img = cv2.imread("Resources/testImage.jpg")

# --- GRAYSCALE ---
# in openCV, convert image to grayscale using COLOR_BGR2GRAY
# in open CV color images are BGR instead of RGB
'''
imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image", imgGrayscale)
cv2.waitKey(0)
'''

# --- BLURRED IMAGE ---
# ksize = kernel size must be odd number (5,5), (7, 7) etc
'''
imgBlurred = cv2.GaussianBlur(img, (7, 7), 0)
cv2.imshow("Blurred Image", imgBlurred)
cv2.waitKey(0)
'''

# --- EDGE DETECTION ---
# Canny(img, threshold1, threshold2)
kernel = np.ones((5,5), np.uint8)

imgCanny = cv2.Canny(img, 100, 100)
# cv2.imshow("Canny Image", imgCanny)
# The most basic morphological operations are dilation and erosion.
# Dilation adds pixels to the boundaries of objects in an image,
# while erosion removes pixels on object boundaries.

# DILATION: THICKEN EDGES
# the more iterations, the thicker the edges
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
#cv2.imshow("Thick edges", imgDialation)
#cv2.waitKey(0)

# EROSION: MAKE EDGES THINNER
# the more iterations, the thicker the edges
imgEroded = cv2.erode(imgDialation, kernel, iterations=1)
cv2.imshow("Thin edges", imgEroded)
cv2.waitKey(0)