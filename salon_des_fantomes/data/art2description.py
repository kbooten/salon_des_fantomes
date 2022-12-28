with open('art.txt','r') as f:
  artworks = [a.rstrip("\n") for a in f.readlines()]

art_and_description = []

import gpt_interface
import time

prompt = "Describe %s. Don't interpret this, just describe it so that somebody who is blind could imagine what it looks like. 50 to 150 words.\n%s is"


for art in artworks:
    time.sleep(.5)
    complete_prompt = prompt % (art,art)
    description = gpt_interface.gpt3_from_prompt(complete_prompt,max_tokens=300,temperature=0.3)
    description = description.replace("\n"," ")
    description = description.strip("\n ")
    art_and_description.append((art,description))


with open('art_and_description.txt','w') as f:
    for art,description in art_and_description:
        f.write(art+"\n")
        f.write(description+"\n\n")