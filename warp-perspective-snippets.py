import cv2
import numpy as np

# --- WARPING IMAGE ---
# Image warping is the process of digitally manipulating an image
# such that any shapes portrayed in the image have been significantly
# distorted. Warping may be used for correcting image distortion
# https://en.wikipedia.org/wiki/Image_warping

# Example: make ace of spades on the table look like the image would have been taken directly above
img = cv2.imread("Resources/cards.jpeg")
width, height = 250, 350
print(img)

# points of corners of the card to be cropped
points1 = np.float32([[119, 103], [320, 83], [159, 399], [377, 363]])
# points of output image
points2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

matrix = cv2.getPerspectiveTransform(points1, points2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("Image", img)
cv2.imshow("Output", imgOutput)
cv2.waitKey(0)