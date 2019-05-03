
"""Adds the missing lang on <html> tag. Note: if the webpafe has multiple languages in the same text, 
this function does NOT add a <span> tag to wrap the text that is in a different language than the html page"""


"""snippet examples:
<html class=\"b-header--black--white b-pw-1280 b-reith-sans-font orb-js id-svg b-reith-sans-loaded bbcdotcom ads-enabled flexbox flexboxlegacy flexwrap svg inlinesvg fontface csscolumns csscolumns-width csscolumns-span csscolumns-fill csscolumns-gap csscolumns-rule csscolumns-rulecolor csscolumns-rulestyle csscolumns-rulewidth csscolumns-breakbefore csscolumns-breakafter csscolumns-breakinside cssgradients supports cssfilters csstransforms generatedcontent bbcdotcom-init bbcdotcom-responsive bbcdotcom-async bbcdotcom-ads-enabled orb-more-loaded gr__bbc_com wwhp-js bbcdotcom-group-2\" style=\"\">
<html class=\"gr__lorientlejour_com\">
<html class=\"gr__aljazeera_net\">
<html class=\"gr__theuselessweb_com\">
<html class=\"gr__m_facebook_com\" data-autoid=\"autoid_6\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" class=\"gr__blombank_com fancybox-margin fancybox-lock\">"""

"""The pattern to find the website url is to search for gr__url_domain"""

from bs4 import BeautifulSoup
from langdetect import detect
import requests #using lateral.io

def run(tag_data):
    snippet = tag_data["snippet"]  # get snippet from bs obj
    # get the url from the BeatifulSoup snippet
    snippet = tag_data["snippet"]
    start_index = snippet.index("gr__") + 4  # to get the start of the url
    half_snippet = snippet[start_index:]  # filter first half
    endpoint = half_snippet.replace("_", ".")
    if (" " in endpoint):
        end_index = endpoint.index(" ")
    elif("\"" in endpoint):
        end_index = endpoint.index("\"")
    url = "https://" + endpoint[:end_index] + "/"  # final url

    querystring = {"url": "{url}"} 
    headers = {
        "subscription-key": "b992e1e8f82f4abf861191895e5f4a1f",#we registered on lateral.io and got our api token
        "content-type": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring) #extract sample text from the webpage
    snippet = "<html lang=\"" + detect(response.text) + "\">"#detect language and return html lang tag
    #print(snippet)
    tag_data["snippet"] = snippet
    return tag_data

