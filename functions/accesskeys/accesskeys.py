from bs4 import BeautifulSoup
from string import ascii_lowercase, ascii_uppercase


def run(html):
    """Takes as input a list of all parsed html strings which include interactive html elements
    and adds an "accesskey" attribute to each one"""
    char = list(ascii_lowercase) + list(ascii_uppercase)
    out = []
    for code in html:  # Iterating over each html string
        # Deserializing the html string
        soup = BeautifulSoup(code, "html.parser")
        # Iterates over all html tags in the string
        for i in soup.findAll():
            if not i.has_attr('accesskey'):
                # Assigns the first available character to the created 'accesskey' value
                i['accesskey'] = char.pop(0)
        out.append(str(soup.prettify()))
    # .prettify returns a list of serilized and formatted html string
    return out
