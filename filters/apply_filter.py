# Description: Apply filters to the image and save it back to the same file.
# Kevin McAleer February 2023

from PIL import Image
import pilgram

# pilgram.inkwell(im).show()

def apply_filters(image_file):
    """ Apply filters to the image and save it back to the same file. """

    # load the image
    im = Image.open(image_file)

    # apply the filters and save the image
    pilgram.toaster(im).save(image_file)
    

def addoverlay(background_file, foreground_file, output_image):
    """ Add an overlay to the background image. """

    background = Image.open(background_file)
 
    # resize the foreground image
    base_width = 640
    img = Image.open(foreground_file)
    img_width, img_height = img.size
    width_percent = (base_width / float(img_width))
    horizontal_size = int((float(img_height) * float(width_percent)))
    foreground = img.resize((base_width,horizontal_size), Image.Resampling.LANCZOS)

    # paste the foreground image on the background and save the image
    background.paste(foreground, (0, 0), foreground)
    background.save(output_image)
    

