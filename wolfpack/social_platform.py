# Base class for social platforms

class SocialPlatform:
    name = "platform name"
    username = "username"
    password = "password"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_message(self, message_text, image_path):
        raise NotImplementedError

