import json

import pilgram
from PIL import Image

from wolfpack import factory, loader

input_image_file = "ohh_hello.jpg"
output_image_file = "ohh_hello_output.jpg"
image = Image.open(input_image_file)

text = "Just found a Raspberry Pi Zero and a Pico hiding in a box. Thats a win, right there. #rasbperrypi"

# pilgram._1977(im).show()
pilgram.toaster(image).save(output_image_file)

# load the social platforms
with open("./wolfpack/social_platforms.json") as f:
    social_platforms = json.load(f)

    loader.load_plugin(social_platforms["platforms"])

platforms = [factory.create(item) for item in social_platforms["items"]]

print(f"Platforms: {platforms}")

for item in platforms:
    print(f"Sending message to {item.name}")
    item.send_message(text, output_image_file)
