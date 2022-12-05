from dotenv import load_dotenv
import os
load_dotenv('.env') 
api_key = os.environ.get("openai")
import re

import openai
openai.api_key = api_key

def gpt3_from_prompt(prompt,temperature=0.9,max_tokens=150,presence_penalty=2.0,frequency_penalty=2.0):
    openai_json = openai.Completion.create(model="text-davinci-002", prompt=prompt, 
                                temperature=temperature, 
                                max_tokens=max_tokens,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                                )
    choice = openai_json['choices'][0]
    finish_text = choice['text']
    print("PROMPT: %s" % prompt)
    finish_text = general_clean(finish_text)
    print("FINISH TEXT: %s" % finish_text)
    return finish_text

def general_clean(text):
    text = text.replace('\n'," ")
    text = re.sub(r' {2,}',' ',text)#text.replace("  "," ")
    text = text.rstrip(" ")
    return text

def main():
    prompt = "The captial of France is"
    print(prompt+gpt3_from_prompt(prompt,max_tokens=5)) 

if __name__ == '__main__':
    main()