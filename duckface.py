from cvzone.HandTrackingModule import HandDetector
import cv2

video = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:

    success, img = video.read()

    hands, img = detector.findHands(img)

    total_fingers = 0

    if hands:
        hand1 = hands[0]

        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1 = hand1["type"]

        fingers = detector.fingersUp(hand1)
        total_fingers = sum(fingers)

        if fingers == [0,0,0,1,1]:
            gesture = "peace"

    cv2.imshow("image", img)
    cv2.waitKey(1)

video.release()
cv2.destroyAllWindows()

