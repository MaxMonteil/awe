from bs4 import BeautifulSoup
from string import ascii_letters, digits as ascii_digits


def run(html):
    """
    Adds accesskey attribute to all interactive HTML elements.

    In case there are more Tags than accesskey characters, only assign keys to the
    first len(alphanum_keys) Tags. Prevents KeyError from alphanum_keys.pop() if
    empty. Normally a page shouldn't need that many acceskeys anyway.

    Parameters:
        html <list> Dictionary with HTML snippets as strings
    Return:
        <list> List of beautiful soup tags with proper accesskey attributes
    """
    htmlTags = [
        BeautifulSoup(item["snippet"], "html.parser").find() for item in html
    ]

    alphanum_keys = available_keys(htmlTags)

    return add_keys(htmlTags, alphanum_keys)


def available_keys(htmlSnippets):
    """
    Clarifies which keys are available to assign to the HTML tags.

    Parameters:
        htmlSnippets <list> BS4 tags
    Return:
        alphanum_keys <set> Characters available to assign as accesskeys
    """
    alphanum_keys = set(ascii_letters + ascii_digits)
    for tag in htmlSnippets[:len(alphanum_keys)]:
        if tag.has_attr("accesskey"):
            if set(tag.get_attribute_list("accesskey")).issubset(alphanum_keys):
                # Removes already used accesskey values from the alphanumbet list
                alphanum_keys.difference_update(
                    set(tag.get_attribute_list("accesskey"))
                )
            else:
                # This key was already removed and is a duplicate
                tag["accesskey"] = ""

    return alphanum_keys


def add_keys(htmlTags, keyMap):
    """
    Adds available keys from the key map to the HTML tags.

    Parameters:
        htmlTags <list> BS4 tags
        keyMap <set> Available access key characters
    Return:
        out <list> BS4 tags with accesskey attributes
    """
    out = []
    for tag in htmlTags[:len(keyMap)]:
        if (not tag.has_attr("accesskey")) or tag["accesskey"] == "":
            # Assigns an arbitrary character to the created 'accesskey' value
            tag["accesskey"] = keyMap.pop()

        out.append(tag)

    return out
