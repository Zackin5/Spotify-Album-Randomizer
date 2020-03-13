from PIL import Image
import numpy as np
import colorama
import ANSILut

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
# ASCII_CHARS = ['.',',',':',';','+','*','%','S','#']
# ASCII_CHARS = ['.',':',';','s','*','o','S','O','X','H','0']
# ASCII_CHARS = ['.',':','^','"','~','c','v','o','*','w','S','O','8','Q','0','#']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100, filter=Image.BICUBIC):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width * 0.5)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim, filter)
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
            char = ASCII_CHARS[charPix//buckets]
            fgColor = ANSILut.Color_To_Ansi_Fore3(fgColorPix[0], fgColorPix[1], fgColorPix[2])
            bgColor = ANSILut.Color_To_Ansi_Back(bgColorPix[0], bgColorPix[1], bgColorPix[2])
            print("{}{}{}".format(fgColor,bgColor,char), sep='', end='')
        print(colorama.Style.RESET_ALL)

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100):
    bgImage = resize(image, new_width, Image.LANCZOS)
    fgImage = resize(image, new_width, Image.NEAREST)
    lutImage = grayscalify(bgImage)

    draw(lutImage, fgImage, bgImage)

