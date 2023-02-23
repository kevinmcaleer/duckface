import instabot
from secret import username, password

bot = instabot.Bot()

# Login to Instagram
bot.login(username=username, password=password)

# This is a test of Duckface, sent via Instabot
bot.upload_photo("duckface.jpg", caption="This is a test of Duckface, sent via Instabot")

