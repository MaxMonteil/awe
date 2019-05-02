from bs4 import BeautifulSoup

def run(tag_data):
    snippet = tag_data["snippet"]
    snippet.find('label')['for'] = snippet.find('input').get('id')
    return tag_data
