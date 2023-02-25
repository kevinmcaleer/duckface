from cvzone.HandTrackingModule import HandDetector
import cv2
from datetime import datetime, timedelta
from picamera2 import Picamera2, Preview
from PIL import Image
from time import sleep
from filters import apply_filters, addoverlay
from wolfpack import factory, loader
import json

# setup camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
picam2.start()

photo_file = 'snap.jpg'
input_image_file = photo_file
output_image_file = "post.jpg"
image = Image.open(input_image_file)

text = "This is the first end-to-end test from Bubo-2T, detecting the hand gesture, taking a picture applying a filter and overlay, and posting to Twitter and IG!"

def detect_gesture():
    # picam2.start()
    
    # video = cv2.VideoCapture(0)
    
    # setup hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    count = 0
    gesture = ""
    start_time = datetime.now()
    target = datetime.today() + timedelta(seconds=1)
    countdown_started = False

    while count < 3:
        current_time = datetime.now()
        # success, img = video.read()
        
        img = picam2.capture_array()
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands, img = detector.findHands(rgb)

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
        
    # cv2.imwrite("snap.jpg", img)
    # video.release()
    cv2.destroyAllWindows()

# Take picture!
def take_picture():
    print("Take picture")
    # picam2 = Picamera2()
    # print("ok1")
    # preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    # picam2.configure(preview_config)

    # picam2.start_preview(Preview.QTGL)

    # picam2.start()
    # print("ok2")
    # time.sleep(0.1)
    # picam2.resolution = (1920, 1080)
    metadata = picam2.capture_file(photo_file)
    print(metadata)
    # picam2.resolution = (640, 480)

    # picam2.close()

# load the social platforms
with open("./wolfpack/social_platforms.json") as f:
    social_platforms = json.load(f)

    loader.load_plugin(social_platforms["platforms"])

platforms = [factory.create(item) for item in social_platforms["items"]]

print(f"Platforms: {platforms}")

while True:
    detect_gesture()
    sleep(2)
    take_picture()
    apply_filters(photo_file)
    addoverlay(photo_file, "overlay.png", output_image_file)
    image = Image.open(photo_file)
    image.show()

    for item in platforms:
        print(f"Sending message to {item.name}")
        item.send_message(text, output_image_file)
