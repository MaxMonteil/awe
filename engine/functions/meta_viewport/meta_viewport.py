from bs4 import BeautifulSoup


def run(tag_data):
    """
    Ensures that the user-scalable="no" parameter is not present in 
    the <meta name="viewport"> element and the maximum-scale parameter 
    is not less than 2.

    Parameters:
        html <list> Dictionaries with HTML snippets as strings
    Return:
        <list> List of beautiful soup proper <meta> tags
    """
    snippet = tag_data["snippet"]
    out = []
    # Remove "user-scalable=no if exists in the "content" attribute
    if "user-scalable" in snippet["content"]:
        start = snippet["content"].find("user-scalable")
        end = snippet["content"].find("no", start) + 2
        end += 1 if snippet["content"][end+1] == "," else 0
        snippet["content"] = snippet["content"].replace(
            snippet["content"][start:end], "")
    # Sets "maximum-scale" to be at least = 2
    if not "maximum-scale" in snippet["content"]:
        snippet["conent"] = snippet["content"] + ", maximum-scale=2"
    scaleIndex = snippet["conent"].find("maximum-scale")+14
    scale = int(scaleIndex)
    scale = 2 if scale < 2 else scale
    snippet["content"] = snippet["content"].replace(
        snippet["content"][scaleIndex:scaleIndex+1], scale)
    tag_data["snippet"] = snippet
    return tag_data
