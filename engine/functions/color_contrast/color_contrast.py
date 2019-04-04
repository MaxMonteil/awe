from bs4 import BeautifulSoup

def run(html):
    """
    Modifies the background and foreground color of text content to
    increase the contrast. Defaults to black on white.
    
    Parameters:
        html <list> Dictionary with HTML snippets as strings
    Return:
        <list> List of beautiful soup tags with proper CSS contrast elements
    """
    htmlTags = [BeautifulSoup(item["snippet"], "html.parser").find()
                for item in html]
    out = []
    for tag in htmlTags:
        if not tag.has_attr("style"):
            tag["style"] = ""
        else:
            #removes pre-existing background-color inline-CSS
            if "background-color" in tag["style"]:
                s = tag["style"].find("background-color") #Index of background-color
                e = tag["style"].find(";", s) + 1 #Index if the following semi-colon
                tag["style"] = tag["style"].replace(tag["style"][s:e], "")
            #removes pre-existing background-color inline-CSS
            if "color" in tag["style"]:
                s = tag["style"].find("color")
                e = tag["style"].find(";", s) + 1
                tag["style"] = tag["style"].replace(tag["style"][s:e], "")
        tag["style"] += "background-color: white; color: black;"
        out.append(tag)
    return out