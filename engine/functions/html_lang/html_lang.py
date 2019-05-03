"""Adds the missing lang on <html> tag. Note: if the webpage has multiple languages in the same text, 
this function does NOT add a <span> tag to wrap the text that is in a different language than the html page"""

from bs4 import BeautifulSoup
from langdetect import detect
from collections import namedtuple

TEXT_TAGS = ["p", "h1", "h2", "h3", "h4", "b", "i", "title", "a", "input"]


def run(data):
    """
    Adds the missing and proper lang attribute on <html> tag.

    Parameters:
        data <namedtuple> That has a bs4 object of the full (html) and a dictionary of (tag_data)
    Return:
        data <namedtuple> With the fixed full HTML
    """
    lang = detect(find_text(data.html))
    if (not data.html.find("html").has_attr("lang")) or data.html.find("html")[
        "lang"
    ] != lang:
        data.html.find("html")["lang"] = lang
    return data


def find_text(bs):
    """
    Helper function that returns a maximum of 300 words from a given BeautifulSoup object

    Parameters:
        bs <bs4> parent bs4 object
    Return:
        <string> a maximum of 300 words
    """
    text = ""
    for tag in TEXT_TAGS:
        if tag == "input":
            for htmlTag in bs.find_all(tag):
                text += (
                    htmlTag["placeholder"] if htmlTag.has_attr("placeholder") else ""
                )
        else:
            for htmlTag in bs.find_all(tag):
                text += htmlTag.get_text() + " "
                if len(text.split()) >= 300:
                    return text
    return text
