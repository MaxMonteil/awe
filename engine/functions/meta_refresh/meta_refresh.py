#!/usr/bin/env python3
"""
Remove the http-equiv="refresh" attribute from each meta element in which it is present.

Type: Direct Function
Info: https://dequeuniversity.com/rules/axe/3.2/meta-refresh
"""

from bs4 import BeautifulSoup


def run(html):
    # find all meta tags
    for meta in html.find_all("meta"):
        if meta.get("http-equiv") and meta["http-equiv"].lower() == "refresh":
            del meta["http-equiv"]
    # if present, remove the http-equiv="refresh" attribute
    return html
