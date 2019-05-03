from bs4 import BeautifulSoup
from rake_nltk import Rake
import nltk
import random

TEXT_TAGS = ["p", "h1", "h2", "h3", "h4", "b", "i", "title", "a"]

def run(data):
    """
    Adds a title to a webpage if it is missing one.

    The function generates a title based on keywords extracted
    from the text contained in the html.

    Parameters:
        Full HTML code for webpage <string>
    Return:
        title tag <BeautifulSoup>
    """
    text = find_text(data.html)  # text extraction line (should be string or list of words)
    wordCount = 0
    for item in text:
        wordCount += len(item.split())
    if wordCount >= 250:
        fix = title(text)  # the title in string format
        tag = BeautifulSoup("<title>" + fix + "</title>", "html.parser")
        data.html.head.append(tag)
        return data  # returns modified html
    else:
        return data

def title(text):
    """
    Extracts keywords from the HTML text and constructs a title.

    Parameters:
        text <list> strings contained in tags
    Return:
        title <string>
    """
    r = Rake(min_length=4, max_length=14)  # Rake instance
    keywords = []
    for e in text:
        r.extract_keywords_from_text(e)
        result = r.get_ranked_phrases()
        if result:
            cand = nltk.pos_tag(
                nltk.word_tokenize(result[0])
            )  # filters out candidates for keywords and pairs them with their respective POS tags
            for c in cand:
                if ("NN" in c or "NNS" in c or "NNP" in c or "NNPS" in c) and (
                    len(c[0]) > 2
                ):
                    keywords.append(
                        c[0]
                    )  # extracts nouns, plural nouns, proper nouns, and proper plural nouns
        else:
            continue
    title = ""
    if len(keywords) <= 4:
        for w in keywords:
            if keywords[-1] == w:
                title = title + w + "."
                return title
            else:
                title = title + w + ", "
    else:
        i = random.sample(range(len(keywords)), 4)
        title = (
            ""
            + keywords[i[0]]
            + ", "
            + keywords[i[1]]
            + ", "
            + keywords[i[2]]
            + ", "
            + keywords[i[3]]
            + "."
        )  # constructs a string out of the most relevant keywords
        return title

def find_text(bs):
    """
    Helper function that returns the text from a given BeautifulSoup object

    Parameters:
        bs <bs4> parent bs4 object
    Return:
        <string> 
    """
    texts = []
    for tag in TEXT_TAGS:
        for htmlTag in bs.find_all(tag):
            texts.append(htmlTag.get_text())
            
    return texts