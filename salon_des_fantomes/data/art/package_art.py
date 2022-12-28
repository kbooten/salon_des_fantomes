art_and_description_tuples = []

with open('art_and_description.txt','r') as f:
	all_text = f.read()

pair_strings = all_text.split("\n\n")

for p in pair_strings:
	pair = p.split("\n")
	print(pair)
	if len(pair)==2:
		art_and_description_tuples.append(tuple(pair))

import json
with open('art_and_description.json','w') as f:
	json.dump(art_and_description_tuples,f)

