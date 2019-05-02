# Temporary run function to make testing possible
# By actully having a run function defined it can be called in a pipeline

import csv

def run(tag_data):
    snippet = tag_data["snippet"]

    # Modifications to the BeautifulSoup tag 
    get_val = snippet["id"]
    snippet['id']=get_val+'1'
    
    tag_data["snippet"] = snippet
    return tag_data
