# Description: This file contains the functions that apply the filters to the images.
# Kevin McAleer February 2023

from PIL import Image, ImageOps
from PIL import ImageFilter

def blur(input_image, output_image):
    """ Apply a blur filter to the image."""
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.BLUR)
    filtered_image.save(output_image)

def contour(input_image, output_image):
    """ Apply a contour filter to the image."""
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.CONTOUR)
    filtered_image.save(output_image)

def autocontrast(input_image, output_image, cutoff=0, ignore=None):
    """ Apply an autocontrast filter to the image."""
    image = Image.open(input_image)
    converted_image = ImageOps.autocontrast(image, cutoff, ignore)
    converted_image.save(output_image)
    
