from bs4 import BeautifulSoup

def run(tag_data):
    snippet = tag_data["snippet"]

    if (snippet.find("table",{'summary':'layout table'})):
       for tr in snippet.findAll('tr'):
          if (snippet.table.tr.th):
             snippet.table.tr.decompose()

    elif (snippet.find("table",{'summary':''})):
       del snippet.table['summary']

    for caption in snippet.findAll('caption'):
       caption.decompose()
    
    tag_data["snippet"] = snippet
    return tag_data
