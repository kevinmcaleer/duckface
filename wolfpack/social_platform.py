# Base class for social platforms

class SocialPlatform:
    name = "platform name"
    username = "username"
    password = "password"

    def __init__(self, username, password):
        """ Initialize the social platform."""
        self.username = username
        self.password = password

    def send_message(self, message_text, image_path):
        """ Send a message to the social platform."""
        raise NotImplementedError

