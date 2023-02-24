from PIL import Image

image = Image.open('duckface.jpg')
image.show('duckface')

def make_sepia_palette(color):
    palette = []
    r, g, b = color
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        palette.extend((new_red, new_green, new_blue))

    return palette

def create_sepia(input_image_path, output_image_path):
    whitish = (255, 240, 192)
    sepia = make_sepia_palette(whitish)

    color_image = Image.open(input_image_path)

    # convert to grayscale
    gray = color_image.convert('L')

    # apply sepia palette
    gray.putpalette(sepia)

    # convert back to color so we can save it as JPEG
    sepia_image = gray.convert('RGB')

    sepia_image.save(output_image_path)

if __name__ == '__main__':
    create_sepia('duckface.jpg', 'duckface_sepia.jpg')
