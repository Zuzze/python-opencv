
import cv2
from utils import stackImages

img = cv2.imread("Resources/cards.jpeg")
imgGrayscale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# stack of images scaled to 50% of original image size
# define stacks as array of rows in matrix
imgStack = stackImages(0.5, ([img, imgGrayscale, img], [img, img, img]))
cv2.imshow("ImageStack", imgStack)

# --- STACK IMAGES ---
# using numpy
'''
horizontalStack = np.hstack((img, img))
verticalStack = np.vstack((img, img))

cv2.imshow("Horizontal", horizontalStack)
cv2.imshow("Vertical", verticalStack)
'''

cv2.waitKey(0)