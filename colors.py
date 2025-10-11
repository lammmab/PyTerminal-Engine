import random
import re
"""
    Colors-
    A simple way to in-line a color in your text
    - Uses regex to find color codes
    - Converts helper colors to their hex codes
    - Outputs text with specificed colors

    Codes:
    * /c - begins the color
    * /c#HEX - use a hex-code
    * /cBLACK - black
    * /cRED - red
    * /cYELLOW - yellow
    * /cGREEN - green
    * /cBLUE - blue
    * /cPURPLE - purple/magenta
    * /cCYAN - cyan
    * /cWHITE - white
    * /cRAND - random
"""

NAMED_COLORS = {
    "BLACK": "#000000",
    "RED": "#FF0000",
    "GREEN": "#00FF00",
    "YELLOW": "#FFFF00",
    "BLUE": "#0000FF",
    "PURPLE": "#800080",
    "CYAN": "#00FFFF",
    "WHITE": "#FFFFFF",
    "ORANGE": "#FFA500",
}

SPECIAL_CODES = ["RAND"]

color_names = list(NAMED_COLORS.keys()) + SPECIAL_CODES

def text_to_color_tuples(text):
    """Converts text to tuples containing hex codes and their text"""
    result = []
    pattern = re.compile(
    r'/c(#([0-9a-fA-F]{6})|' + '|'.join(color_names) + r')',
    re.IGNORECASE # only match hex codes or color names
    )
    matches = list(pattern.finditer(text))

    if not matches:
        return None

    for i,match in enumerate(matches):
        _start, end = match.span()
        color_code = match.group()

        next_start = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        after_text = text[end:next_start]

        color_code = color_code.replace("/c","")

        if color_code == "RAND":
            color_code = f"#{random.randint(0, 0xFFFFFF):06X}"
        elif color_code in NAMED_COLORS:
            color_code = NAMED_COLORS[color_code]
        elif not re.fullmatch(r'#[0-9A-F]{6}', color_code):
            color_code = "#FFFFFF" # fallback to white

        result.append((color_code, after_text))
    return result

def hex_to_rgb(hex_color):
    """Helper to convert hex codes to rgb"""
    hex_color = hex_color.lstrip('#')

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)

def color_tuples_to_ansi_text(color_tuples):
    """Converts colors + text to formatted text"""
    final_text = ""
    for piece in color_tuples:
        code,text = piece
        r,g,b = hex_to_rgb(code)
        final_text += f"\x1B[38;2;{r};{g};{b}m{text}\x1B[0m"
    return final_text

def parse_colors(text):
    """Main function to call: Outputs converted text with colors"""
    color_tuples = text_to_color_tuples(text)
    if not color_tuples:
        return text
    colored_text = color_tuples_to_ansi_text(color_tuples)
    return colored_text + "\x1B[0m"
if __name__ == "__main__":
    print(parse_colors("/cRANDI love text!"))
