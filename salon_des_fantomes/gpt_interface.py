from dotenv import load_dotenv
import os
load_dotenv('.env') 
api_key = os.environ.get("openai")
import re

import openai
openai.api_key = api_key

def gpt3_from_prompt(prompt,temperature=0.9,max_tokens=400,presence_penalty=2.0,frequency_penalty=2.0,model="text-davinci-002",stop=None):
    openai_json = openai.Completion.create(model=model, prompt=prompt, 
                                temperature=temperature, 
                                max_tokens=max_tokens,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                                stop=stop,
                                )
    choice = openai_json['choices'][0]
    finish_text = choice['text']
    print("PROMPT: %s" % prompt)
    finish_text = general_clean(finish_text)
    print("FINISH TEXT: %s" % finish_text)
    return finish_text

# def gpt3_edit(input,instruction,temperature=0.7):
#     openai_json = openai.Edit.create(model="text-davinci-edit-001",
#                                 input=input,
#                                 instruction=instruction,
#                                 temperature=temperature, 
#                                 )
#     choice = openai_json['choices'][0]
#     finish_text = choice['text']
#     finish_text = general_clean(finish_text)
#     return finish_text

def general_clean(text):
    #text = text.replace('\n'," ") ##
    text = re.sub(r' {2,}',' ',text)#text.replace("  "," ")
    text = text.rstrip(" \n")
    return text

def main():
    prompt = "The capital of France is"
    print(prompt+gpt3_from_prompt(prompt,max_tokens=5)) 
    #input = "you are so charming.  would you like to come for dinner?"
    #instruction = 'Invent a Finno-Bantoid language called Nrattat.  Translate the input text into this language.'
    #print(gpt3_edit(input=input,instruction=instruction))

if __name__ == '__main__':
    main()