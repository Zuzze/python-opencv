import cv2
import numpy as np

# zero = colored pixel
# 3 => color channels (if not defined is grayscale)
img = np.zeros((512, 512, 3), np.uint8)
print(img)

# --- SQUARE IMAGE BACKGROUND ---
# [:] => whole image displayed (all cols and rows of matrix)
# 255, 0, 0 => Blue image
'''
img[:] = 255,0,0
cv2.imshow("Image", img)
cv2.waitKey(0)
'''

# --- GREEN LINE ---
# (img, startPoint, endPoint, lineColor, thickness)
# cv2.line(img, (0,0), (300, 300), (0, 255, 0), 3)
# make line to fill whole image
cv2.line(img, (0,0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)

# --- RECTANGLE ---
# unfilled rectangle
# cv2.rectangle(img, (0,0), (250, 350), (0,0,255), 2)
# filled rectangle
cv2.rectangle(img, (0,0), (250, 350), (0,0,255), cv2.FILLED)

# --- CIRCLE ---
# (centerPoint, radius, color, thickness)
cv2.circle(img, (400, 50), 30, (255, 255, 0), 5)

# --- TEXT ---
# putText(img, myText, startPoint, font, fontSize, fontColor, fontWeight)
cv2.putText(img, "OPENCV", (300, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 150, 0), 3)

# Display image
cv2.imshow("Image", img)
cv2.waitKey(0)