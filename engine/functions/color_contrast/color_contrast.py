"""
The function first checks whether the text color is closer to white/black
then lightens/darkens the text until the contrast is enough for AAA WCAG.

If changing the text color wasn't enough it will darken/lighen the
background color until the contrast is enough for AAA WCAG.
"""
from bs4 import BeautifulSoup
import wcag_contrast_ratio as contrast


def run(html):
    """
    Modifies the background and foreground color of text content and background
    to increase the contrast.
    
    Parameters:
        html <list> Dictionaries with HTML snippets as strings and hexadecimal
            color of the background and foreground
    Return:
        <list> List of beautiful soup tags with proper CSS contrast elements
    """
    out = []
    for item in html:
        back = hex_to_rgb(item["colors"]["background"])
        fore = hex_to_rgb(item["colors"]["foreground"])
        
        backLight = is_light(back)  #True if the background is closer to white than black
        cond = {"contrast":contrast.rgb([x/255 for x in back], [x/255 for x in fore]) <= 4.5,
            "notLightest":max(fore) < 255 or backLight, 
            "notDarkest":fore != [0, 0, 0] or not backLight}
        while(all(cond.values())):
            fore = [
                color + (-min([10, color]) if backLight else min(10, 255-color)) for color in fore]
            cond["contrast"] = contrast.rgb([x/255 for x in back], [x/255 for x in fore]) <= 4.5
            cond["notLightest"] = max(fore) < 255 or backLight
            cond["notDarkest"] = fore != [0, 0, 0] or not backLight
        #Now we adjust the conditions to the background colors
        cond["notLightest"] = max(back) < 255 or not backLight
        cond["notDarkest"] = back != [0, 0, 0] or backLight
        while(all(cond.values())):
            back = [color + (min(10, 255-color) if backLight else (-min([10, color]))) for color in back]
            cond["contrast"] = contrast.rgb([x/255 for x in back], [x/255 for x in fore]) <= 4.5
            cond["notLightest"] = max(back) < 255 or not backLight
            cond["notDarkest"] = back != [0, 0, 0] or backLight
        tag = BeautifulSoup(item["snippet"], "html.parser").find()
        if not tag.has_attr("style"):
            tag["style"] = ""
        else:
            #removes pre-existing background-color inline-CSS
            if any(x in tag["style"] for x in ["background-color", "background"]):
                # Index of background-color
                s=tag["style"].find("background-color")
                # Index if the following semi-colon
                e=tag["style"].find(";", s) + 1
                tag["style"]=tag["style"].replace(tag["style"][s:e], "")
                s = tag["style"].find("background")
                tag["style"] = tag["style"].replace(tag["style"][s:e], "")
            #removes pre-existing background-color inline-CSS
            if "color" in tag["style"]:
                s=tag["style"].find("color")
                e=tag["style"].find(";", s) + 1
                tag["style"]=tag["style"].replace(tag["style"][s:e], "")
        tag["style"] += "background-color: #%s; color: #%s;" % (rgb_to_hex(back), rgb_to_hex(fore))
        out.append(tag)
    return out

def hex_to_rgb(hexValue):
    """
    Parameters:
        String hexadecimal value of color
    Return:
        <list> RGB color values respectively
    """
    return list(int(hexValue[i:i+2], 16) for i in range(0, 6, 2))

def rgb_to_hex(RGBValues):
    """
    Parameters:
        <list> RGB color values respectively
    Return:
        String hexadecimal value of color
    """
    return '%02x%02x%02x' % tuple(RGBValues)

def is_light(RGB):
    """
    Parameters:
        <list> RGB color values respectively
    Return:
        bool whether the color is closer to white than black
    """
    return (255-max(RGB) < min(RGB))

h = [{"colors": {
        "background": "00a408",
        "foreground": "fffff8"
        },
    "selector": "#signup-button",
      "snippet": """<a role="button" class="_5t3c _28le btn btnS medBtn mfsm touchable" id="signup-button" tabindex="0"
    data-sigil="m_reg_button" data-autoid="autoid_3" style="background:#00a408; color:#fffff8;">Create New Account</a>"""
    },
    {"colors": {
        "background": "eceff8",
        "foreground": "7596c8"
        },
    "selector": "#forgot-password-link",
    "snippet": """<a tabindex="0"
    href="/recover/initiate/?c=https%3A%2F%2Fm.facebook.com%2F%3Frefsrc%3Dhttps%253A%252F%252Fwww.facebook.com%252F&amp;r&amp;cuid&amp;ars=facebook_login&amp;lwv=100&amp;refid=8"
    id="forgot-password-link" style="background:#eceff8; color:#7596c8;">Forgotten password?</a>"""
    }]

for ht in run(h):
    print(ht.prettify())
