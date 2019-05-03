from bs4 import BeautifulSoup

def run(tag_data):
    snippet = tag_data["snippet"]
    soup = BeautifulSoup(str(snippet),'html.parser')
    label = soup.new_tag("label")
    label["for"] = snippet.get('name')
    label.string = str(snippet.get('name'))
    soup.append(label)
    tag_data["snippet"] = soup
    return tag_data
