from colorama import Fore, Back, Style

# 2x2x2 Foreground LUT
LUT_FORE2 = [[[Fore.BLACK,Fore.GREEN],[Fore.RED,Fore.YELLOW]],[[Fore.BLUE,Fore.CYAN],[Fore.MAGENTA,Fore.WHITE]]]

# 3x3x3 Foreground LUT
LUT_FORE3 = [[[Fore.BLACK, Fore.GREEN, Style.BRIGHT+Fore.GREEN], [Fore.RED, Fore.RED, Fore.GREEN], [Style.BRIGHT+Fore.RED, Fore.RED, Style.BRIGHT+Fore.YELLOW]],
[[Fore.BLUE, Fore.CYAN, Fore.CYAN], [Style.BRIGHT+Fore.BLUE, Fore.WHITE, Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Fore.WHITE]],
[[Fore.BLUE, Fore.CYAN, Style.BRIGHT+Fore.CYAN], [Fore.MAGENTA, Fore.WHITE, Style.BRIGHT+Fore.CYAN], [Style.BRIGHT+Fore.MAGENTA, Fore.MAGENTA, Style.BRIGHT+Fore.WHITE]]]

# 2x2x2 Background LUT
LUT_BACK = [[[Back.BLACK,Back.GREEN], [Back.RED,Back.YELLOW]],
[[Back.BLUE,Back.CYAN], [Back.MAGENTA,Back.WHITE]]]

def Float_To_Index(f, cutoff = 0.5):
    return int(f/256 > cutoff)

def Color_To_Ansi_Fore2(r, g, b):
    return LUT_FORE2[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]

def Color_To_Ansi_Fore3(r, g, b):
    return LUT_FORE3[Float_To_Index(b, 0.33)][Float_To_Index(r, 0.33)][Float_To_Index(g, 0.33)]

def Color_To_Ansi_Back(r, g, b):
    return LUT_BACK[Float_To_Index(b)][Float_To_Index(r)][Float_To_Index(g)]