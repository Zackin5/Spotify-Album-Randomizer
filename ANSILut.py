from colorama import Fore, Back, Style
from PIL import Image
import json

# Load config
with open('conf.json') as json_file:
    conf = json.load(json_file)
    art_method = 0
    art_hi_pal = False

    if 'art_method' in conf:
        art_method = conf['art_method']

    if 'art_method' in conf:
        art_method = conf['art_method']

    if 'art_hi_palette' in conf:
        art_hi_pal = conf['art_hi_palette']


# 2x2x2 Foreground LUT
LUT_FORE2 = [[[Fore.BLACK,Fore.GREEN],[Fore.RED,Fore.YELLOW]],[[Fore.BLUE,Fore.CYAN],[Fore.MAGENTA,Fore.WHITE]]]

# 3x3x3 Foreground LUT
LUT_FORE3 = [[[Fore.BLACK,Fore.GREEN,Fore.GREEN],[Fore.RED,Fore.YELLOW,Fore.GREEN],[Fore.RED,Fore.YELLOW,Fore.YELLOW]],
            [[Fore.BLUE,Fore.BLUE,Fore.GREEN],[Fore.MAGENTA,Fore.BLUE,Fore.GREEN],[Fore.RED,Fore.RED,Fore.YELLOW]],
            [[Fore.BLUE,Fore.BLUE,Fore.CYAN],[Fore.MAGENTA,Fore.MAGENTA,Fore.CYAN],[Fore.MAGENTA,Fore.MAGENTA,Fore.WHITE]]]

# 3x3x3 Foreground LUT (BRIGHT lookups)
LUT_FORE3_BRIGHT = [[[Fore.BLACK, Fore.GREEN, Style.BRIGHT+Fore.GREEN], [Fore.RED, Fore.RED, Fore.GREEN], [Style.BRIGHT+Fore.RED, Fore.RED, Style.BRIGHT+Fore.YELLOW]],
[[Fore.BLUE, Fore.CYAN, Fore.CYAN], [Style.BRIGHT+Fore.BLUE, Fore.WHITE, Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Fore.WHITE]],
[[Fore.BLUE, Fore.CYAN, Style.BRIGHT+Fore.CYAN], [Fore.MAGENTA, Fore.WHITE, Style.BRIGHT+Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Style.BRIGHT+Fore.WHITE]]]

# 2x2x2 Background LUT
LUT_BACK2 = [[[Back.BLACK,Back.GREEN], [Back.RED,Back.YELLOW]],
            [[Back.BLUE,Back.CYAN], [Back.MAGENTA,Back.WHITE]]]

# 3x3x3 Background LUT
LUT_BACK3 = [[[Back.BLACK,Back.GREEN,Back.GREEN],[Back.RED,Back.YELLOW,Back.GREEN],[Back.RED,Back.YELLOW,Back.YELLOW]],
            [[Back.BLUE,Back.BLUE,Back.GREEN],[Back.MAGENTA,Back.WHITE,Back.GREEN],[Back.RED,Back.RED,Back.YELLOW]],
            [[Back.BLUE,Back.BLUE,Back.CYAN],[Back.MAGENTA,Back.MAGENTA,Back.CYAN],[Back.MAGENTA,Back.MAGENTA,Back.WHITE]]]

# ANSI Palette for conversion
ANSI_PAL = [0,0,0, 192,0,0, 0,192,0, 0,0,192, 192,192,0, 192,0,192, 0,192,192, 192,192,192]
# ANSI_PAL = [0,0,0, 255,0,0, 0,255,0, 0,0,255, 255,255,0, 255,0,255, 0,255,255, 255,255,255]
ANSI_PAL_BRIGHT = [0,0,0, 128,0,0, 0,128,0, 0,0,128, 128,128,0, 128,0,128, 0,128,128, 192,192,192,
                    255,0,0, 0,255,0, 255,255,0, 0,0,255, 255,0,255, 0,255,255, 224,224,224]

def Float_To_Index(f, lutDimension = 2):
    return int(f/(256/lutDimension))

def Color_To_Ansi_Fore(colorPix):
    r = colorPix[0]
    g = colorPix[1]
    b = colorPix[2]
    
    if art_hi_pal:
        return LUT_FORE3_BRIGHT[Float_To_Index(b, 3)][Float_To_Index(r, 3)][Float_To_Index(g, 3)]
    else:
        return LUT_FORE2[Float_To_Index(b, 2)][Float_To_Index(r, 2)][Float_To_Index(g, 2)]

def Color_To_Ansi_Back(colorPix):
    r = colorPix[0]
    g = colorPix[1]
    b = colorPix[2]
    
    return LUT_BACK2[Float_To_Index(b, 2)][Float_To_Index(r, 2)][Float_To_Index(g, 2)]

def Image_To_Ansi_Pal(img):
    pal = Image.new('P', img.size)
    pal.putpalette(ANSI_PAL * 32)
    
    img = img.convert('RGB')
    
    palImage = img.quantize(palette=pal, dither=0)

    return palImage.convert('RGB')
    
def Image_To_Ansi_Pal_Fore(img):
    pal = Image.new('P', img.size)

    if art_hi_pal:
        pal.putpalette(ANSI_PAL_BRIGHT * 17)
    else:
        pal.putpalette(ANSI_PAL * 32)
    
    img = img.convert('RGB')
    
    palImage = img.quantize(palette=pal, dither=0)

    return palImage.convert('RGB')
    