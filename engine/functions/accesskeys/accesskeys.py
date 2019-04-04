from bs4 import BeautifulSoup
from string import ascii_letters, digits as ascii_digits


def run(html):
    """
    Adds accesskey attribute to all interactive HTML elements.

    Parameters:
        html <list> List of html code snippets of string type
    Return:
        <list> List of beautiful soup items with proper accesskey attributes
    """
    alphanum_keys = set(ascii_letters + ascii_digits)

    # Snippets always only have one tag
    htmlTags = [
        BeautifulSoup(node["snippet"], "html.parser").find() for node in html["items"]
    ]

    out = []

    # In case there are more Tags than accesskey characters, only assign keys to the
    # first len(alphanum_keys) Tags. Prevents KeyError from alphanum_keys.pop() if
    # empty. Normally a page shouldn't need that many acceskeys anyway.
    for tag in htmlTags[:len(alphanum_keys)]:
        if tag.has_attr("accesskey"):
            if set(tag.get_attribute_list("accesskey")).issubset(alphanum_keys):
                # Removes already used accesskey values from the alphanumbet list
                alphanum_keys.difference_update(
                    set(tag.get_attribute_list("accesskey"))
                )
            else:
                # This key was already removed and is a duplicate, assign a new one
                tag.get_attribute_list("accesskey").append(alphanum_keys.pop())

        else:
            # Assigns an arbitrary character to the created 'accesskey' value
            tag.get_attribute_list("accesskey").append(alphanum_keys.pop())

        out.append(tag)

    return out
