import cv2

print("OpenCV Imported")

# --- IMPORT IMAGE ---
# imread = image read
'''
img = cv2.imread("Resources/testImage.jpg")
cv2.imshow("Output", img)
cv2.waitKey(0)
'''

# --- IMPORT VIDEO ---
# Video is a sequence of images
# break the sequence and quit video by pressing q key
'''
cap = cv2.VideoCapture("Resources/testVideo.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

# --- USE WEBCAM ---
# param for VideoCapture is the id of web cam
# in windows this is apparently 0, on mac this was 1
# press q to quit the stream
# see more at https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html
cap = cv2.VideoCapture(1)
# set webcam width (id=3)
cap.set(3, 640)
# set webcam height (id=4)
cap.set(4, 480)
# set brightness (id=10)
cap.set(10, 100)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break