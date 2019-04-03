# Takes json and return html
import json


# read file
with open('Parse_OLJ.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)

# show values
print( str(obj['items']['node']['snippet']))
