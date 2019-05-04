from bs4 import BeautifulSoup
from cssutils import parseStyle


def run(tag_data):
    snippet = tag_data["snippet"]

    for anchor in snippet.findAll("a"):
        anchor["aria-label"] = anchor.text
        anchor.string.replace_with("[Read more...]")

    for anchor in snippet.findAll("a", attrs={"style": True}):
        anchorStyle = parseStyle(anchor["style"])
        if anchorStyle["display"] == "none":
            del anchorStyle["display"]
        del anchorStyle["aria-hidden"]
        anchor["style"] = anchorStyle.cssText

    for anchor in snippet.findAll("a", attrs={"onmouseout": True}):
        anchor["onblur"] = anchor["onmouseout"]

    for anchor in snippet.findAll("a", attrs={"onmouseover": True}):
        anchor["onfocus"] = anchor["onmouseover"]

    tag_data["snippet"] = snippet
    return tag_data
