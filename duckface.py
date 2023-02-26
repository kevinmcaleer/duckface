import json
from datetime import datetime, timedelta
from time import sleep

from toot_randomiser import RandomToots
import cv2
from cvzone.HandTrackingModule import HandDetector
from picamera2 import Picamera2
# from libcamera import Transform
import libcamera
from PIL import Image

from filters import addoverlay, apply_filters
from wolfpack import factory, loader

from pydub import AudioSegment
from pydub.playback import play

# DEBUG = True # True doesn't post to social networks
DEBUG = False

# setup camera
picam2 = Picamera2()
picam2.rotation = 180

picam2.preview_configuration.size = (800,600)
preview_config = picam2.create_preview_configuration(transform = libcamera.Transform(hflip=1, vflip=1))
picam2.create_still_configuration = (2304,1296)
sensor_w, sensor_h = picam2.sensor_resolution
picam2.configure(picam2.create_preview_configuration(main={"size": (640,480)}, transform=libcamera.Transform(vflip=1, hflip=1)))
picam2.configure(picam2.create_video_configuration(transform=libcamera.Transform(vflip=1, hflip=1)))

picam2.start()

# Define the image files
PHOTO_FILE = 'snap.jpg'
INPUT_IMAGE_FILE = PHOTO_FILE
OUTPUT_IMAGE_FILE = "post.jpg"

image = Image.open(INPUT_IMAGE_FILE)

random_message = RandomToots()

text = random_message.text

def play_toot_sound():
    """ Play toot sound """
    song = AudioSegment.from_mp3('toot.mp3')
    play(song)

def detect_gesture():
    
    count = 0
    # setup hand detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    target = datetime.today() + timedelta(seconds=1)
    countdown_started = False

    while count < 3:
        current_time = datetime.now()
        
        img = picam2.capture_array()
        # img = picam2.capture_image("main")
        # bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # rgb = Image.fromarray(img)
        hands, img = detector.findHands(rgb)
        # hands, img = detector.findHands(img)
        cv2.imshow("image", img)
        cv2.waitKey(1)

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
    
        
        
    # cv2.destroyAllWindows()


def take_picture():
    """Take picture """
    
    print("Taking picture")
   

    picam2.switch_mode_and_capture_file("still", PHOTO_FILE)

    # metadata = picam2.capture_file(PHOTO_FILE)
    # print(metadata)


# load the social platforms
with open("./wolfpack/social_platforms.json") as f:
    social_platforms = json.load(f)

    loader.load_plugin(social_platforms["platforms"])

platforms = [factory.create(item) for item in social_platforms["items"]]

print(f"Platforms: {platforms}")

while True:
    detect_gesture()
    # sleep(2)
    play_toot_sound()
    take_picture()
    # sleep(0.1)
    print('fixing image rotation for bubo-2t images')
    image = Image.open(PHOTO_FILE)
    image = image.rotate(180)
    image = image.save(PHOTO_FILE)
    # sleep(0.1)
    apply_filters(PHOTO_FILE)
    addoverlay(PHOTO_FILE, "overlay4608x2592.png", OUTPUT_IMAGE_FILE)
    image = Image.open(OUTPUT_IMAGE_FILE)
    image.show()

    if not DEBUG:
        for item in platforms:
            print(f"Sending message to {item.name}")
            item.send_message(text, OUTPUT_IMAGE_FILE)

cv2.destroyAllWindows()