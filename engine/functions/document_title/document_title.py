from bs4 import BeautifulSoup
from rake_nltk import Rake
import nltk
def run(html):
    """
    Adds a title to a webpage if it is missing one.

    The function generates a title based on keywords extracted
    from the text contained in the html.

    Parameters:
        Full HTML code for webpage <string>
    Return:
        title tag <BeautifulSoup>
    """
    soup = html
    text = [p.get_text() for p in soup.find_all("p", text=True)] # filters out the text
	title = title(text) # the title in string format
    (soup.title).string = title
    return soup # returns modified html
    
	

def title(text):
    """
    Extracts keywords from the HTML text and constructs a title.

    Parameters:
        a list of texts contained in <p> tags
    Return:
        title <string>
    """
    r = Rake(min_length=4, max_length=14) # Rake instance
    keywords = []
    for e in text:
        r.extract_keywords_from_text(e)
        result = r.get_ranked_phrases()
        if result:
            cand = nltk.pos_tag(nltk.word_tokenize(result[0])) # filters out candidates for keywords and pairs them with their respective POS tags
            for c in cand:
                if ('NN' in c or 'NNS' in c or 'NNP' in c or 'NNPS' in c) and (len(c[0]) > 2):
                    keywords.append(c[0]) # extracts nouns, plural nouns, proper nouns, and proper plural nouns
        else:
            continue
    title = ""+keywords[1]+", "+keywords[2]+", "+keywords[3]+", "+keywords[-3] # constructs a string out of the most relevant keywords
    return title