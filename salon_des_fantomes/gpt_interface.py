from dotenv import load_dotenv
import os

load_dotenv('.env') 

api_key = os.environ.get("openai")

import openai
openai.api_key = api_key


import re

from nltk import tokenize


def possibly_emergency_cut_prompt(prompt,max_tokens,total_max=3800):
    while len(tokenize.word_tokenize(prompt))+max_tokens>total_max:
        prompt = prompt.split(" ",1)[1] ## take away 0th token
    return prompt


def gpt3_from_prompt(prompt,temperature=0.7,max_tokens=500,presence_penalty=0,frequency_penalty=0,model="text-davinci-003",stop=">"):
    prompt = possibly_emergency_cut_prompt(prompt,max_tokens)
    openai_json = openai.Completion.create(model=model, prompt=prompt, 
                                temperature=temperature, 
                                max_tokens=max_tokens,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                                stop=stop, #trying suffix instead of stop
                                #suffix=suffix
                                )
    choice = openai_json['choices'][0]
    finish_text = choice['text']
    print("PROMPT: %s" % prompt)
    finish_text = general_clean(finish_text)
    print("FINISH TEXT: %s" % finish_text)
    return finish_text


def general_clean(text):
    #text = text.replace('\n'," ") ##
    text = re.sub(r' {2,}',' ',text)#text.replace("  "," ")
    text = text.rstrip(" \n")
    text = text.replace("\n"," ")
    # if text.endswith(">")==False:
    #     text+=">"
    return text


def main():
    prompt = "The capital of France is"
    print(prompt+gpt3_from_prompt(prompt,max_tokens=5)) 
    #input = "you are so charming.  would you like to come for dinner?"
    #instruction = 'Invent a Finno-Bantoid language called Nrattat.  Translate the input text into this language.'
    #print(gpt3_edit(input=input,instruction=instruction))


if __name__ == '__main__':
    main()