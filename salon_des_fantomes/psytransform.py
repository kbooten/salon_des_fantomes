import random,time,re

from gpt_interface import gpt3_from_prompt#,gpt3_edit

def transform(text, prompt,stop=">"):
    prompt = prompt % text ## replaces '%s' in prompt, adds prefix character
    return gpt3_from_prompt(prompt,stop=stop)


def transform_text(text,prompt,probability_of_transformation):
    if random.random()<probability_of_transformation:
        text = transform(text,prompt)
        time.sleep(.3)
    return text


from psychotropics.utterance_transformers import transformation_odd_parenthetical,transformation_expand_into_simple_words,transformation_doubt,transformation_juan

transformations = [transformation_odd_parenthetical,transformation_expand_into_simple_words,transformation_doubt,transformation_juan]
import time

def main():
    test_text = "Once I met someone who liked to smell burning hair.  They ended up leaving and moving to Alaska."
    #transformation_probability_tuples = [(add_odd_parenthetical,2.3)]
    for trans in transformations:
        text = transform_text(test_text,trans.prompt,1.0) 
        print(text)
        time.sleep(1)

if __name__ == '__main__':
  main()