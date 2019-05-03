#!/usr/bin/env python3

"""
The function first checks whether the text color is closer to white/black
then lightens/darkens the text until the contrast is enough for AA WCAG.

If changing the text color wasn't enough it will darken/lighen the
background color until the contrast is enough for AA WCAG.
"""
from bs4 import BeautifulSoup
import wcag_contrast_ratio as contrast


RGB_LIMIT = 255
COLOR_STEP = 10


def run(tag_data):
    """
    Modifies the background and foreground color of text content and background
    to increase the contrast.

    Parameters:
        tag_data <dict> Data of the faulty tag
    Return:
        <dict> Data of the fixed tag
    """
    back = hex_to_rgb(tag_data["colors"]["background"])
    fore = hex_to_rgb(tag_data["colors"]["foreground"])  # Text color

    # True if the background is closer to white than black
    backLight = is_light(back)

    # Set initial conditions for the foreground text color
    cond = {
        "contrast": not contrast.passes_AA(
            contrast.rgb(
                [v / RGB_LIMIT for v in back], [v / RGB_LIMIT for v in fore]
            )
        ),
        "notLightest": max(fore) < RGB_LIMIT or backLight,
        "notDarkest": all(fore) or not backLight,
    }

    # Loop to adjust the foreground colors
    while all(cond.values()):
        fore = [
            color
            + (
                -min(COLOR_STEP, color)
                if backLight
                else min(COLOR_STEP, RGB_LIMIT - color)
            )
            for color in fore
        ]

        cond["contrast"] = not contrast.passes_AA(
            contrast.rgb(
                [v / RGB_LIMIT for v in back], [v / RGB_LIMIT for v in fore]
            )
        )
        cond["notLightest"] = max(fore) < RGB_LIMIT or backLight
        cond["notDarkest"] = all(fore) or not backLight

    # Now we adjust the conditions to the background colors
    cond["notLightest"] = max(back) < RGB_LIMIT or not backLight
    cond["notDarkest"] = all(back) or backLight

    # Loop to adjust the background colors
    while all(cond.values()):
        back = [
            color
            + (
                min(COLOR_STEP, RGB_LIMIT - color)
                if backLight
                else -min(COLOR_STEP, color)
            )
            for color in back
        ]

        cond["contrast"] = not contrast.passes_AA(
            contrast.rgb(
                [v / RGB_LIMIT for v in back], [v / RGB_LIMIT for v in fore]
            )
        )
        cond["notLightest"] = max(back) < RGB_LIMIT or not backLight
        cond["notDarkest"] = all(back) or backLight

    snippet = tag_data["snippet"][0]
    if not snippet.has_attr("style"):
        snippet["style"] = ""

    backChanged = rgb_to_hex(back) != tag_data["colors"]["background"]

    # Remove "background-color" styles if its color was changed
    if backChanged and "background-color" in snippet["style"]:
        start = snippet["style"].find("background-color")
        end = snippet["style"].find(";", start) + 1
        snippet["style"] = snippet["style"].replace(snippet["style"][start:end], "")

    # Remove "background" styles if its color was changed
    if backChanged and "background" in snippet["style"]:
        start = snippet["style"].find("background")
        end = snippet["style"].find(";", start) + 1
        snippet["style"] = snippet["style"].replace(snippet["style"][start:end], "")

    # Remove "color" styles
    if "color" in snippet["style"]:
        start = snippet["style"].find("color")
        end = snippet["style"].find(";", start) + 1
        snippet["style"] = snippet["style"].replace(snippet["style"][start:end], "")

    # Add the new calculated styles
    snippet["style"] += f"color: #{rgb_to_hex(fore)}; "
    snippet["style"] += f"background: #{rgb_to_hex(back)}; " if backChanged else ""

    tag_data["snippet"][0] = snippet

    return tag_data


def hex_to_rgb(hexValue):
    """
    Parameters:
        String hexadecimal value of color
    Return:
        <tuple> RGB color values
    """
    return list(int(hexValue[i : i + 2], 16) for i in range(0, 6, 2))


def rgb_to_hex(RGBValues):
    """
    Parameters:
        <list> RGB color values respectively
    Return:
        <str> String hexadecimal value of color
    """
    return "%02x%02x%02x" % tuple(RGBValues)


def is_light(RGB):
    """
    Parameters:
        <list> RGB color values respectively
    Return:
        <bool> whether the color is closer to white than black
    """
    return RGB_LIMIT - max(RGB) < min(RGB)
