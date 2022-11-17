from dotenv import load_dotenv
import os
load_dotenv('.env') 
api_key = os.environ.get("openai")

import openai
openai.api_key = api_key


def gpt3_from_prompt(prompt,temperature=0.9,max_tokens=70,presence_penalty=2.0,frequency_penalty=2.0):
    openai_json = openai.Completion.create(model="text-davinci-002", prompt=prompt, 
                                temperature=temperature, 
                                max_tokens=max_tokens,
                                presence_penalty=presence_penalty,
                                frequency_penalty=frequency_penalty,
                                )
    choice = openai_json['choices'][0]
    finish_text = choice['text']
    finish_text = general_clean(finish_text)
    return finish_text


def general_clean(text):
    return text.replace('\n\n',"")

def main():
    prompt = "The captial of France is "
    print(prompt+gpt3_from_prompt(prompt,max_tokens=5)) 

if __name__ == '__main__':
    main()