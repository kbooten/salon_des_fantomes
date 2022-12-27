import random,time,re

from gpt_interface import gpt3_from_prompt#,gpt3_edit

def transform(text, prompt):
    prompt = prompt % text ## replaces '%s' in prompt, adds prefix character
    return gpt3_from_prompt(prompt,stop=">")


def transform_text(text,prompt,probability_of_transformation,max=3):
    c = 0
    while probability_of_transformation>0 and c<max:
        if random.random()<probability_of_transformation:
            text = transform(text,prompt,stop=">")
            print('transforming')
            time.sleep(.3)
            print(text)
        else:
            break
        c+=1
        probability_of_transformation-=1.0 ## decrement (maybe by less)
    return text

def main():
    from psychotropics.utterance_transformers import expand_into_simple_words as pt 
    test_text = "Once I met someone who liked to smell burning hair.  They ended up leaving and moving to Alaska."
    #transformation_probability_tuples = [(add_odd_parenthetical,2.3)]
    text = transform_text(test_text,pt.prompt,2.0) 
    print(text)

if __name__ == '__main__':
  main()