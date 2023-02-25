from PIL import Image
import pilgram

# pilgram.inkwell(im).show()

def apply_filters(image_file):
    im = Image.open(image_file)
    # pilgram._1977(im).show()
    pilgram.toaster(im).save(image_file)
    # pilgram.toaster(im).show()
    

def addoverlay(background_file, foreground_file, output_image):
    background = Image.open(background_file)
    # foreground = Image.open(foreground_file)

    basewidth = 640
    img = Image.open(foreground_file)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    foreground = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)

    background.paste(foreground, (0, 0), foreground)
    background.save(output_image)
    # background.show()

