from colorama import Fore, Back, Style
from PIL import Image
import json

# Load config
with open('conf.json') as json_file:
    conf = json.load(json_file)
    art_method = 0

    if 'art_method' in conf:
        art_method = conf['art_method']


# 2x2x2 Foreground LUT
LUT_FORE2 = [[[Fore.BLACK,Fore.GREEN],[Fore.RED,Fore.YELLOW]],[[Fore.BLUE,Fore.CYAN],[Fore.MAGENTA,Fore.WHITE]]]

# 3x3x3 Foreground LUT
LUT_FORE3 = [[[Fore.BLACK, Fore.GREEN, Style.BRIGHT+Fore.GREEN], [Fore.RED, Fore.RED, Fore.GREEN], [Style.BRIGHT+Fore.RED, Fore.RED, Style.BRIGHT+Fore.YELLOW]],
[[Fore.BLUE, Fore.CYAN, Fore.CYAN], [Style.BRIGHT+Fore.BLUE, Fore.WHITE, Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Fore.WHITE]],
[[Fore.BLUE, Fore.CYAN, Style.BRIGHT+Fore.CYAN], [Fore.MAGENTA, Fore.WHITE, Style.BRIGHT+Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Style.BRIGHT+Fore.WHITE]]]

# 2x2x2 Background LUT
LUT_BACK = [[[Back.BLACK,Back.GREEN], [Back.RED,Back.YELLOW]],
[[Back.BLUE,Back.CYAN], [Back.MAGENTA,Back.WHITE]]]

# ANSI Palette for conversion
ANSI_PAL = [0,0,0, 192,0,0, 0,192,0, 0,0,192, 192,192,0, 192,0,192, 0,192,192, 192,192,192]
ANSI_PAL_BRIGHT = [0,0,0, 128,0,0, 0,128,0, 0,0,128, 128,128,0, 128,0,128, 0,128,128, 192,192,192,
                    255,0,0, 0,255,0, 255,255,0, 0,0,255, 255,0,255, 0,255,255, 224,224,224]

def Float_To_Index(f, cutoff = 0.5):
    return int(f/256 > cutoff)

def Color_To_Ansi_Fore(colorPix):
    r = colorPix[0]
    g = colorPix[1]
    b = colorPix[2]

    if art_method == 0:
        return LUT_FORE2[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]
    elif art_method == 1:
        return LUT_FORE3[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]
    else:
        # Palette conversion
        if r == 128 and g == 0 and b == 0:
            return Fore.RED
        elif r >= 255 and g == 0 and b == 0:
            return Style.BRIGHT+Fore.RED
        elif r == 0 and g == 128 and b == 0:
            return Fore.GREEN
        elif r == 0 and g >= 255 and b == 0:
            return Style.BRIGHT+Fore.GREEN
        elif r == 0 and g == 0 and b == 128:
            return Fore.BLUE
        elif r == 0 and g == 0 and b >= 255:
            return Style.BRIGHT+Fore.BLUE
        elif r == 128 and g == 128 and b == 0:
            return Fore.YELLOW
        elif r >= 255 and g >= 255 and b == 0:
            return Style.BRIGHT+Fore.YELLOW
        elif r == 128 and g == 0 and b == 128:
            return Fore.MAGENTA
        elif r >= 255 and g == 0 and b >= 255:
            return Style.BRIGHT+Fore.MAGENTA
        elif r == 0 and g == 128 and b == 128:
            return Fore.CYAN
        elif r == 0 and g >= 255 and b >= 255:
            return Style.BRIGHT+Fore.CYAN
        elif r == 192 and g == 192 and b == 192:
            return Fore.WHITE
        elif r >= 224 and g >= 224 and b >= 224:
            return Style.BRIGHT+Fore.WHITE
        # elif r >= 128 and g >= 128 and b >= 128:
        #     return Style.BRIGHT+Fore.BLACK
        else:
            return Fore.BLACK

def Color_To_Ansi_Back(colorPix):
    r = colorPix[0]
    g = colorPix[1]
    b = colorPix[2]

    if art_method == 0:
        return LUT_BACK[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]
    elif art_method == 1:
        return LUT_BACK[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]
    else:
        threshold = 128
        
        if r >= threshold and g == 0 and b == 0:
            return Back.RED
        elif r == 0 and g >= threshold and b == 0:
            return Back.GREEN
        elif r == 0 and g == 0 and b >= threshold:
            return Back.BLUE
        elif r >= threshold and g >= threshold and b == 0:
            return Back.YELLOW
        elif r >= threshold and g == 0 and b >= threshold:
            return Back.MAGENTA
        elif r == 0 and g >= threshold and b >= threshold:
            return Back.CYAN
        elif r >= threshold and g >= threshold and b >= threshold:
            return Back.WHITE
        else:
            return Back.BLACK

def Image_To_Ansi_Pal(img):
    pal = Image.new('P', img.size)
    pal.putpalette(ANSI_PAL * 32)
    
    img = img.convert('RGB')
    
    palImage = img.quantize(palette=pal, dither=0)

    return palImage.convert('RGB')
    
def Image_To_Ansi_Pal_Bright(img):
    pal = Image.new('P', img.size)
    pal.putpalette(ANSI_PAL_BRIGHT * 16)
    
    img = img.convert('RGB')
    
    palImage = img.quantize(palette=pal, dither=0)

    return palImage.convert('RGB')
    