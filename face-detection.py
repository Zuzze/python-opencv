import cv2

# --- FACE DETECTION ---
# OpenCV has built-in classifier for face/non-face classification
# 1) img to grayscale
# 2) use face detection classifier via CascadeClassifier()
# 3) create bounding box to detected faces

classifierPath = "Resources/face-detection-classifier.xml"
imgPath = "Resources/group_photo.jpg"
faceCascade = cv2.CascadeClassifier(classifierPath)
img = cv2.imread(imgPath)
imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgScale = 1.1
minNeighbours = 4
faces = faceCascade.detectMultiScale(imgGrayscale, imgScale, minNeighbours)
boundingBoxBorderColor = (255, 0, 0)
boundingBoxBorderWidth = 2

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), boundingBoxBorderColor, boundingBoxBorderWidth)


cv2.imshow("Result", img)
cv2.waitKey(0)