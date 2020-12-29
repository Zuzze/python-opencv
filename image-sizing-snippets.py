import cv2
import numpy as np

img = cv2.imread("Resources/testImage.jpg")
print(img.shape)

# --- RESIZE IMAGE ---
# this stretches image to given (width, height)
imgResize = cv2.resize(img, (300, 200))
# cv2.imshow("Image", img)
# cv2.imshow("Image Resize", imgResize)
# cv2.waitKey(0)
print(imgResize.shape)

# --- CROP IMAGE ---
# note that height before width
# decide the values based on printed shape
imgCropped = img[200:400, 200:500]
cv2.imshow("Image Cropped", imgCropped)
cv2.waitKey(0)