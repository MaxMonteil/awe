from bs4 import BeautifulSoup


def run(tag_data):
    """
    Ensures that the user-scalable="no" parameter is not present in 
    the <meta name="viewport"> element and the maximum-scale parameter 
    is not less than 2.

    Parameters:
        tag_data <dict> Data of the faulty tag
    Return:
        <dict> Data of the fixed tag
    """
    snippet = tag_data["snippet"]
    snippet["content"] = snippet["content"].replace(" ", "")
    # Remove "user-scalable=no if exists in the "content" attribute
    if "user-scalable=no" in snippet["content"]:
        snippet["content"].replace("user-scalable=no", "")
    # Sets "maximum-scale" to be at least = 2
    if not "maximum-scale" in snippet["content"]:
        snippet["content"] = snippet["content"] + ",maximum-scale=2"
    scaleIndexStart = snippet["content"].find("maximum-scale") + 14
    scaleIndexEnd = scaleIndexStart + num_length(snippet["content"][scaleIndexStart:])
    scale = int(snippet["content"][scaleIndexStart:scaleIndexEnd])
    scale = 2 if scale < 2 else scale
    snippet["content"] = snippet["content"].replace(
        snippet["content"][scaleIndexStart:scaleIndexEnd], scale
    )
    tag_data["snippet"] = snippet
    return tag_data


def is_int(n):
    """
    Helper function to determine whether a character is a string or not

    Parameters:
        n <char> 
    Return:
        <bool> True if the character is numeric
    """
    try:
        int(n)
        return True
    except:
        return False


def num_length(full):
    """
    Helper function which, given a string and a starting index, 
    determines how many characters (if any) a number has starting
    at the given index
    
    Parameters:
        full <string> The full containing string
        start <int> Starting index to look at
    Return:
        <int> The number of characters of the number
    """
    length = 0
    while is_int(full[length]) or full[length] == ".":
        length += 1
    return length
