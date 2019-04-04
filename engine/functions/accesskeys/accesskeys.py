from bs4 import BeautifulSoup
from string import ascii_letters, digits as ascii_digits


def run(html):
    """
    Adds accesskey attribute to all interactive HTML elements.

    In case there are more Tags than accesskey characters, only assign keys to the
    first len(alphanum_keys) Tags. Prevents KeyError from alphanum_keys.pop() if
    empty. Normally a page shouldn't need that many acceskeys anyway.

    Parameters:
        <list> List of dicts, this function only needs the "items" values from the dicts
    Return:
        <list> List of beautiful soup items with proper accesskey attributes
    """
    
    htmlTags = [
        BeautifulSoup(item["snippet"], "html.parser") for item in html
    ]

    alphanum_keys = AvailableKeys(htmlTags)

    return AddKeys(htmlTags, alphanum_keys)


def AvailableKeys(htmlSnippets):
    """
    Input:
        list of BS4 objects
    Output:
        A set of characters available to assign to accesskeys
    """

    alphanum_keys = set(ascii_letters + ascii_digits)
    for snippet in htmlSnippets[:len(alphanum_keys)]:
        #Iterates over the HTML's tags. 
        for tag in snippet.findAll():
            if tag.has_attr("accesskey"):
                if set(tag.get_attribute_list("accesskey")).issubset(alphanum_keys):
                    # Removes already used accesskey values from the alphanumbet list
                    alphanum_keys.difference_update(
                        set(tag.get_attribute_list("accesskey"))
                    )
                else:
                    # This key was already removed and is a duplicate. Remove the attribute value
                    tag["accesskey"] = ""
    return alphanum_keys

def AddKeys(htmlSnippets, keyMap):
    """
    Input:
        list of BS4 objects
        set of available chars
    Output:
        A list of BS4 objects with accesskey attributes
    """
    out = []
    for snippet in htmlSnippets[:len(keyMap)]:
        for tag in snippet.findAll():
            if (not tag.has_attr("accesskey")) or tag["accesskey"]=="":
                # Assigns an arbitrary character to the created 'accesskey' value
                tag["accesskey"] = keyMap.pop()
        out.append(snippet)
    return out