from PIL import Image
import pilgram

im = Image.open('ohh_hello.jpg')
# pilgram._1977(im).show()
pilgram.toaster(im).save('ohh_hello_earlybird.jpg')

# pilgram.inkwell(im).show()