from bs4 import BeautifulSoup
from string import ascii_lowercase, ascii_uppercase

def Accesskey(html):
    """takes a list of all parsed html strings which include interactive html elements
    and adds an "accesskey" attribute to each one"""
    char = list(ascii_lowercase) + list(ascii_uppercase)
    for code in html:  # Iterating over each html string
        # Deserializing the html string
        soup = BeautifulSoup(code, "html.parser")
        # Iterates over all html tags in the string
        for i in soup.findAll():
            if not i.has_attr('accesskey'):
                # Assigns the first available character to the created 'accesskey' value
                i['accesskey'] = char.pop(0)
    # .prettify returns a serilized and formatted html string
    return str(soup.prettify())