from bs4 import BeautifulSoup
from string import ascii_lowercase, ascii_uppercase


def run(html):
    """
    Adds accesskey attribute to all interactive HTML elements.

    Input:
        List of HTML strings
    Output:
        List of beautiful soup items with proper accesskey attributes
    """
    htmlSnippets = [
        BeautifulSoup(node["snippet"], "html.parser") for node in html["items"]
    ]
    alpha = AvailableKeys(htmlSnippets)
    return AddKeys(htmlSnippets, alpha)

def AvailableKeys(htmlSnippets):
    """
    Input:
        list of BS4 objects
    Output:
        A list of characters available to assign to accesskeys
    """

    alpha = list(ascii_lowercase + ascii_uppercase)
    # Removes already used accesskey values from the alphabet list
    for snippet in htmlSnippets:
        # Iterates over all html tags in the string
        for i in snippet.findAll():
            if i.has_attr('accesskey'):
                if i['accesskey'][0] in alpha:
                    alpha.remove(i['accesskey'][0])
    return alpha

def AddKeys(htmlSnippets, keyMap):
    """
    Input:
        list of BS4 objects
        list of available chars
    Output:
        A list of BS4 objects with accesskey attributes
    """
    out = []
    # Assigns the first available character to the created 'accesskey' value
    for snippet in htmlSnippets:
        for i in snippet.findAll():
            if not i.has_attr('accesskey'):
                i['accesskey'] = keyMap.pop(0)
        out.append(snippet)
    return out
