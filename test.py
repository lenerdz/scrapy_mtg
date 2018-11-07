import json
from pprint import pprint

with open('data/cardlist.json') as f:
    data = json.load(f)

newdata=[]
x=1
for c in data:
    c['id'] = x
    c['error'] = 0
    newdata.append(c)
    x+=1

with open('data/cardlist.json', 'w') as g:
    json.dump(newdata, g, indent=2)

# for x in data:
#     print(x['name'])
