import json
from datetime import datetime, timedelta
from time import sleep

import cv2
from cvzone.HandTrackingModule import HandDetector
from picamera2 import Picamera2
from PIL import Image

from filters import addoverlay, apply_filters
from wolfpack import factory, loader

# setup camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
picam2.start()

# Define the image files
PHOTO_FILE = 'snap.jpg'
INPUT_IMAGE_FILE = PHOTO_FILE
OUTPUT_IMAGE_FILE = "post.jpg"

image = Image.open(INPUT_IMAGE_FILE)

text = "I made a robot that can see and tweet! This is from the prototype, now to upload this code to Bubo-2T for real.\n #robotics #python #STEM #raspberrypi"

def detect_gesture():
    
    count = 0
    # setup hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    target = datetime.today() + timedelta(seconds=1)
    countdown_started = False

    while count < 3:
        current_time = datetime.now()
        
        img = picam2.capture_array()
        # rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)/
        rgb = Image.fromarray(img)
        hands, img = detector.findHands(rgb)

        if not hands:
            continue

        # A hand is detected
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # Check for peace sign gesture
        if not fingers == [0,1,1,0,0]:
            countdown_started = False
            count = 0
            continue

        # Check for countdown
        if not countdown_started:
            countdown_started = True
            continue

        # check if time is up
        if current_time >= target:
            count += 1
            target = datetime.today() + timedelta(seconds=1)                    
    
        cv2.imshow("image", img)
        cv2.waitKey(1)
        
    cv2.destroyAllWindows()


def take_picture():
    """Take picture """
    
    print("Taking picture")
    metadata = picam2.capture_file(PHOTO_FILE)
    print(metadata)


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
    apply_filters(PHOTO_FILE)
    addoverlay(PHOTO_FILE, "overlay.png", OUTPUT_IMAGE_FILE)
    image = Image.open(PHOTO_FILE)
    image.show()

    for item in platforms:
        print(f"Sending message to {item.name}")
        item.send_message(text, OUTPUT_IMAGE_FILE)
