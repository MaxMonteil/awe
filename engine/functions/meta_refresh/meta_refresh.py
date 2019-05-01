#!/usr/bin/env python3
"""
Remove meta tags with the http-equiv="refresh" attribute.

Type: Direct Function
Info: https://dequeuniversity.com/rules/axe/3.2/meta-refresh
Procedure taken from: https://www.w3.org/TR/2016/NOTE-WCAG20-TECHS-20161007/F41
"""


def run(html):
    # find all meta tags
    for meta in html.find_all("meta"):
        # if present, remove the http-equiv="refresh" attribute
        if (meta.get("http-equiv") and meta["http-equiv"].lower() == "refresh"):
            meta.decompose()

    return html
