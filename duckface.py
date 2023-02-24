from cvzone.HandTrackingModule import HandDetector
import cv2
from datetime import datetime, timedelta
from picamera2 import Picamera2, Preview
from PIL import Image

def detect_gesture():

    # setup camera
    video = cv2.VideoCapture(0)
    
    # setup hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    count = 0
    gesture = ""
    start_time = datetime.now()
    target = datetime.today() + timedelta(seconds=1)
    countdown_started = False

    while count < 3:
        current_time = datetime.now()
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

            if fingers == [0,1,1,0,0]:
                gesture = "peace"
                if countdown_started:
                    if current_time >= target:
                        count += 1
                        target = datetime.today() + timedelta(seconds=1)                    
                else:
                    countdown_started = True
                    start_time = datetime.now()
            else:
                countdown_started = False
                count = 0
                gesture = ""

        # cv2.putText(img, gesture, (10, 115), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        # cv2.putText(img, str(current_time), (10, 215), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 6)
        # cv2.putText(img, str(target), (10, 115), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 6)
        cv2.imshow("image", img)
        cv2.waitKey(1)

    video.release()
    cv2.destroyAllWindows()

# Take picture!
def take_picture():
    picam2 = Picamera2()

    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QTGL)

    picam2.start()
    time.sleep(2)

    metadata = picam2.capture_file("snap.jpg")
    print(metadata)

    picam2.close()


while True:
    detect_gesture()
    take_picture()
    image = Image()
    image.open('snap.jpg')
    image.show()
