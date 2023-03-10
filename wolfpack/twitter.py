import tweepy

from wolfpack import factory
from wolfpack.secret import (twitter_access_token, twitter_access_token_secret,
                             twitter_consumer_key, twitter_consumer_secret)

from .social_platform import SocialPlatform

class Twitter(SocialPlatform):
    name = "Twitter"

    def __init__(self):
        
        # Authenticate to Twitter
        twitter_auth_keys = {
        "consumer_key"        : twitter_consumer_key,
        "consumer_secret"     : twitter_consumer_secret,
        "access_token"        : twitter_access_token,
        "access_token_secret" : twitter_access_token_secret
        }

        self.auth = tweepy.OAuthHandler(
                twitter_auth_keys['consumer_key'],
                twitter_auth_keys['consumer_secret']
                )
        self.auth.set_access_token(
                twitter_auth_keys['access_token'],
                twitter_auth_keys['access_token_secret']
                )
        self.api = tweepy.API(self.auth)

    def send_message(self, message_text, image_path):
        """ Send a message to the social platform. """
       
        media = self.api.media_upload(image_path)

        # Post tweet with image
        post_result = self.api.update_status(status=message_text, media_ids=[media.media_id])
        
        if post_result:
            print("Twitter post sent successfully")
            return True
        else:
            print("Twitter post reported a failure, though this may not be the case.")
            return False

def initialize():
    """ Registers the Twitter social platform. """
    print('Registering Twitter')
    factory.register('twitter', Twitter)