import shutil
import os

from instabot import Bot

from wolfpack import factory
from wolfpack.secret import ig_password, ig_username

from .social_platform import SocialPlatform


class Instagram(SocialPlatform):
    name = "Instagram"

    def __init__(self):
        if os.path.exists('config'):
            shutil.rmtree('config') 
        self.username = ig_username
        self.password = ig_password
        self.bot = Bot()

    def send_message(self, message_text, image_path):
        print("Sending message to Instagram")
        print("Message text: " + message_text)
        print("Image path: " + image_path)

        # Login to Instagram
        self.bot.login(username=self.username, password=self.password)

        # This is a test of Duckface, sent via Instabot
        if self.bot.upload_photo(image_path, caption=message_text):
            print("Instagram post sent successfully")

            # fix the filename renaming that instabot does
            new_name = os.path.basename(image_path + ".REMOVE_ME")
            os.rename(new_name, image_path)
            return True
        else:
            print("Instagram post reported a failure, though this may not be the case.")
            return False

def initialize():
    print('Registering Instagram')
    factory.register('instagram', Instagram)