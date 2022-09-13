from PIL import Image, ImageFilter
import numpy as np
import colorama
from colorama import Style
import ANSILut
import json

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
# ASCII_CHARS = [' ','⋅','⋰','∴','⛆']
# ASCII_CHARS = ['.',',',':',';','+','*','%','S','#']
# ASCII_CHARS = ['.',':',';','s','*','o','S','O','X','H','0']
# ASCII_CHARS = ['.',':','^','"','~','c','v','o','*','w','S','O','8','Q','0','#']
ASCII_CHARS = ASCII_CHARS[::-1]

# Load config
with open('conf.json') as json_file:
    conf = json.load(json_file)
    art_method = 0

    if 'art_method' in conf:
        art_method = conf['art_method']

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100, filterXAxis=Image.BICUBIC, filterYAxis=Image.BILINEAR):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)

    new_height = int(aspect_ratio * new_width)

    # Scale X axis
    x_correct_dim = (new_width, int(max(new_height, old_height / 2)))
    new_image = image.resize(x_correct_dim, filterXAxis)

    # Scale Y axis
    y_correct_dim = (new_width, int(new_height / 2))
    new_image = image.resize(y_correct_dim, filterYAxis)

    return new_image
'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
method draw():
    - replaces every pixel with a character whose intensity is similar
'''
def draw(lutImage, fgColorImage, bgColorImage, buckets=25):
    initial_pixels = np.asarray(lutImage)
    fg_color_pixels = np.asarray(fgColorImage)
    bg_color_pixels = np.asarray(bgColorImage)

    for x in range(len(initial_pixels)):
        for y in range(len(initial_pixels[0])):
            charPix = initial_pixels[x][y]
            
            fgColorPix = fg_color_pixels[x][y]
            bgColorPix = bg_color_pixels[x][y]

            index = max(0, min(charPix//buckets, len(ASCII_CHARS) - 1))

            char = ASCII_CHARS[index]
            fgColor = ANSILut.Color_To_Ansi_Fore(fgColorPix)
            bgColor = ANSILut.Color_To_Ansi_Back(bgColorPix)
            print("{}{}{}".format(fgColor,bgColor,char+Style.NORMAL), sep='', end='')
        print(colorama.Style.RESET_ALL)

def drawDebug(image):
    image = image.resize((100,100), Image.NEAREST)
    image.show()

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100):
    # pre-resize filtering
    image = image.filter(ImageFilter.UnsharpMask)

    # resize
    bgImage = resize(image, new_width, Image.NEAREST, Image.LANCZOS)
    fgImage = resize(image, new_width, Image.NEAREST, Image.NEAREST)
    # drawDebug(bgImage)

    lutImage = image.filter(ImageFilter.FIND_EDGES)
    lutImage = resize(lutImage, new_width, Image.LANCZOS, Image.LANCZOS)
    
    lutImage = grayscalify(bgImage)

    if art_method >= 1:
        bgImage = ANSILut.Image_To_Ansi_Pal(bgImage)
        fgImage = ANSILut.Image_To_Ansi_Pal_Fore(fgImage)

    # drawDebug(fgImage)
    # drawDebug(bgImage)
    
    draw(lutImage, fgImage, bgImage)

