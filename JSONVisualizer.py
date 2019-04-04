import matplotlib.pyplot as plt
import numpy as np
import json

file = open("parsed_audit.json")
json = json.load(file)
audits = [0,0,0]
for e in json:
    if e == "score":
        continue
    elif json[e]["applicable"] == False:
        audits[0] += 1
    elif json[e]["applicable"] == True:
        if json[e]["failing"] == True:
            audits[1] += 1
        else:
            audits[2] += 1

def visualize(l):
# The pie chart
    labels = 'Cannot be tested', 'Failed', 'Passed'
    sizes = l
    explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    colors = ("#444444","#ff931e","#0099cc")
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, colors=colors, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.show()
    
    plt.rcdefaults()
    fig, ax = plt.subplots()

# The bar chart
    objects = ('g', 'f', 'c', 'b', 'a')
    y_pos = np.arange(len(people))
    performance = (1, 4, 3, 2, 8)
    ax.barh(y_pos, performance, align='center', color='red', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(objects)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Level')
    ax.set_title('Criticality')
    plt.show()

visualize(audits)