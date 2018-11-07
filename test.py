import json
from pprint import pprint

with open('cards.json') as f:
    data = json.load(f)

for x in data:
    print(x['name'])
