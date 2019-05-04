from bs4 import BeautifulSoup

def run(data):
    """
    Wraps <dd> and <dt> tags in <dl> tags.

    Parameters:
    data <namedtuple> includes the full (html) and the (tag_data)
    Return:
    data <namedtuple> with the full fixed (html) 
    """
    data.html = items(data.html)
    return data

def items(soup):
    """
    Finds <dt> and <dd> tags, makes <dl> a sibling, then inserts tags in <dl> tag.

    Parameters:
    Full HTML code <soup>
    Return:
    Full HTML code with fixed tags <soup>
    """
    tags = soup.find_all(['dt', 'dd'])
    dltag = BeautifulSoup("<dl></dl>","html.parser").find()
    (tags[0].parent).append(dltag)
    for tag in tags:
        dltag.append(tag)
    return soup