from PIL import Image, ImageOps
from PIL import ImageFilter

def blur(input_image, output_image):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.BLUR)
    filtered_image.save(output_image)

def contour(input_image, output_image):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.CONTOUR)
    filtered_image.save(output_image)

def autocontrast(input_image, output_image, cutoff=0, ignore=None):
    image = Image.open(input_image)
    converted_image = ImageOps.autocontrast(image, cutoff, ignore)
    converted_image.save(output_image)
    

if __name__ == "__main__":
    # contour('duckface.jpg', 'duckface_contour.jpg')
    # image = Image.open('duckface_contour.jpg')
    # image.show('duckface_contour')
    autocontrast('duckface.jpg', 'duckface_autocontrast.jpg', cutoff=0.5)
