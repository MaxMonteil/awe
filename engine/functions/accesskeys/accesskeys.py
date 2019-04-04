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
    # To be assigned to accesskey values
    alpha = list(ascii_lowercase + ascii_uppercase)
    htmlSnippets = [
        BeautifulSoup(node["snippet"], "html.parser") for node in html["items"]
    ]

    out = []
    for snippet in htmlSnippets:
        # Iterates over all html tags in the string
        for i in snippet.findAll():
            if i.has_attr('accesskey'):
                # Removes already used accesskey values from the alphabet list
                alpha.remove(i['accesskey'][0])
            else:
                # Assigns the first available character to the created 'accesskey' value
                i['accesskey'] = alpha.pop(0)

        out.append(snippet)

    return out
