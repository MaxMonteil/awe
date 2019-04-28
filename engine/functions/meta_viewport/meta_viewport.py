from bs4 import BeautifulSoup

def run(html):
    """
    Ensures that the user-scalable="no" parameter is not present in 
    the <meta name="viewport"> element and the maximum-scale parameter 
    is not less than 2.

    Parameters:
        html <list> Dictionaries with HTML snippets as strings
    Return:
        <list> List of beautiful soup proper <meta> tags
    """
    htmlTags = [BeautifulSoup(item["snippet"], "html.parser").find()
                for item in html]
    out = []
    for tag in htmlTags:
        # Remove "user-scalable=no if exists in the "content" attribute
        if "user-scalable" in tag["content"]:
            start = tag["content"].find("user-scalable")
            end = tag["content"].find("no", start) + 2
            end += 1 if tag["content"][end+1] == "," else 0
            tag["content"] = tag["content"].replace(tag["content"][start:end], "")
        # Sets "maximum-scale" to be at least = 2
        if not "maximum-scale" in tag["content"]:
            tag["conent"] = tag["content"] + ", maximum-scale=2"
        scaleIndex = tag["conent"].find("maximum-scale")+14
        scale = int(scaleIndex)
        scale = 2 if scale < 2 else scale
        tag["content"] = tag["content"].replace(
                tag["content"][scaleIndex:scaleIndex+1], scale)
        out.append(tag)
    return out
