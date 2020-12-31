import cv2

# ------- CAR LICENSE PLATE DETECTION --------
# 1) Image to grayscale
# 2) Detect contours
# 3) Use Cascade classifier


# CONFIG
frameWidth = 640
frameHeight = 480
nPlateCascade = cv2.CascadeClassifier("Resources/license_plate_classifier.xml")
minArea = 200
color = (255, 0, 255)

# VIDEO INPUT CONFIG
cap = cv2.VideoCapture(1)
# set webcam width (id=3)
cap.set(3, frameWidth)
# set webcam height (id=4)
cap.set(4, frameHeight)
# set brightness (id=10)
cap.set(10, 150)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            # add bounding box (rectangle on top of license plates)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            fontSize = 1
            fontWeight = 2
            cv2.putText(img,
                        "Number Plate",
                        (x, y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        fontSize,
                        color,
                        fontWeight
            )
            # Crop bounding box
            # ROI = Region of interest = bounding box
            numberPlate = img[y:y+h, x:x+w]
            cv2.imshow("ROI", numberPlate)

    cv2.imshow("Result", img)


    # save scanned license plate by pressing S key
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Resources/Scanned_License_Plates/Plate_" + str(count) + ".jpg", numberPlate)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                    2, (0, 0, 255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1