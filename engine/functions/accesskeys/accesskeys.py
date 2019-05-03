from bs4 import BeautifulSoup
from string import ascii_letters, digits as ascii_digits


def run(tag_data):
    """
    Adds accesskey attribute to all interactive HTML elements.

    In case there are more Tags than accesskey characters, only assign keys to the
    first len(alphanum_keys) Tags. Prevents KeyError from alphanum_keys.pop() if
    empty. Normally a page shouldn't need that many acceskeys anyway.

    Parameters:
        tag_data <dict> Data of the faulty tag
    Return:
        <dict> Data of the fixed tag
    """
    snippet = tag_data["snippet"][0]
    
    alphanum_keys = available_keys(snippet)
    if (not snippet.has_attr("accesskey")) or snippet["accesskey"] == "":
        snippet["accesskey"] = alphanum_keys.pop()    
    tag_data["snippet"][0] = snippet

    return tag_data


def available_keys(tag):
    """
    Clarifies which keys are available to assign to the HTML tags.

    Parameters:
        tag <bs4>
    Return:
        alphanum_keys <set> Characters available to assign as accesskeys
    """
    alphanum_keys = set(ascii_letters + ascii_digits)
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