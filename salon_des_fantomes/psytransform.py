import random,time,re

from gpt_interface import gpt3_from_prompt#,gpt3_edit

def transform(text, prompt,stop=">"):
    prompt = prompt % text ## replaces '%s' in prompt, adds prefix character
    return gpt3_from_prompt(prompt,stop=stop)


def transform_text(text,prompt,probability_of_transformation):
    if random.random()<probability_of_transformation:
        text = transform(text,prompt)
        print('transforming')
        time.sleep(.3)
    return text

def main():
    from psychotropics.utterance_transformers import odd_parenthetical as pt 
    test_text = "Once I met someone who liked to smell burning hair.  They ended up leaving and moving to Alaska."
    #transformation_probability_tuples = [(add_odd_parenthetical,2.3)]
    text = transform_text(test_text,pt.prompt,2.0) 
    print(text)

if __name__ == '__main__':
  main()