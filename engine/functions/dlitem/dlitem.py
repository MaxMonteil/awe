from bs4 import BeautifulSoup


def run(data):
    """
    Wraps <dd> and <dt> tags in <dl> tags.

    Input:
    Full HTML code <soup>
    Output:
    Full HTML code with fixed tags <soup>
    """
    soup = data.html
    items(soup)

def items(soup):
    """
    Finds <dt> and <dd> tags, makes <dl> a sibling, then inserts tags in <dl> tag.
    Input:
    Full HTML code <soup>
    Output:
    Full HTML code with fixed tags <soup>
    """
    tags = soup.find_all(['dt', 'dd'])
    dltag = BeautifulSoup("<dl></dl>","html.parser").find()
    (tags[0].parent).append(dltag)
    for tag in tags:
        dltag.append(tag)
    print(dltag.parent.parent)
    return soup