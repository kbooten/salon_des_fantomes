import random

import persons
characters = persons.get_people()

import drinks

from data import questions
questions = questions.questions
random.seed("salon")
#random.shuffle(questions) ##

from dialogue import Dialogue
from description import DescriptionAdder#,starting_drinks,later_drinks


import time # for file naming

import dill as pickle

import json

from termcolor import colored


class Salon:


  def __init__(self,questions,characters,drinks):
    self.questions = questions
    self.characters = characters
    self.all_drinks = drinks
    self.min_people = 4
    self.max_people = 7#len(self.characters)
    self.number_of_dialogue_turns = 10
    ## saving output
    self.file_prefix = "output/output"
    self.output_file = self.get_file_name()
    ## adding drinks
    self.create_drink_file() 
    self.current_drinks = []

  def create_drink_file(self,limit=False):
    """
    by default psychotropic drinks are disabled
    """
    with open('drinks.txt','w') as f:
        for d in self.all_drinks:
          if limit==True:
            if self.all_drinks[d]==None:
                f.write(d+"\n")
            else:
                f.write('#'+d+"\n")
          else:
            f.write(d+"\n")
    input("Check drinks.txt? (ENTER to continue)")


  def set_current_drinks(self):
    """
    load drinks, ignoring commented out
    """
    with open('drinks.txt','r') as f:
      all_drinks = [l.strip() for l in f.readlines()]
      allowed_drinks = [d for d in all_drinks if d.startswith("#")==False]
      self.current_drinks = {key:val for key,val in self.all_drinks.items() if key in allowed_drinks}
      print("\ncurrently serving %d drinks:\n%s\n" % (len(self.current_drinks.keys())," - ".join(self.current_drinks.keys())))


  def get_file_name(self):
    """
    return a new file name
    """
    y,mo,d,h,min = time.localtime()[:5] # 
    return "%s_%d-%d-%d_%d~%d.txt" % (self.file_prefix,mo,d,y,h,min)


  def get_rough_word_count(self):
    """
    return number of words, roughly
    """
    with open(self.output_file,'r') as f:
      text = f.read()
    tokens = text.split(' ')
    words = [t for t in tokens if any(c.isalpha() for c in t)]
    return len(words)


  def get_subset_of_characters(self):
    """
    return a random subset characters, but always include Socrates and Player
    """
    mandatory = [char for char in self.characters if (char.is_player==True or char.name=="Socrates")]
    other_possibilities = [char for char in characters if char not in mandatory] ## all other possibilities
    n_to_select = random.randrange(self.min_people,self.max_people) - len(mandatory)
    others_chosen = random.sample(other_possibilities,n_to_select)
    subset_of_characters = others_chosen+mandatory
    return subset_of_characters

  def write_output(self,text):
    """
    write to file
    """
    try: ## adding to file
      f = open(self.output_file,'a')
      print('writing to %s' % self.output_file)
    except FileNotFoundError: ## new file
      print('creating %s' % self.output_file)
      f = open(self.output_file,'w')
    f.write(text)
    f.close()


  def new_dialogue(self):
    """
    generate and output a new conversation
    """
    next_question = self.questions.pop(0) ## cycle through, 
    self.questions.append(next_question)  ##  infinitely 
    subset_of_characters = self.get_subset_of_characters()
    description_adder = DescriptionAdder(subset_of_characters,self.current_drinks)
    current_dialogue = Dialogue(subset_of_characters,next_question,description_adder)
    n = input("How many dialogue turns? (enter a number, or leave empty for default--%d)" % self.number_of_dialogue_turns)
    if n!="":
      try:
        self.number_of_dialogue_turns = int(n)
      except:
        pass
    current_dialogue.generate(n=self.number_of_dialogue_turns)
    print(current_dialogue.current_text)
    self.write_output("CHAPTER n\n"+current_dialogue.current_text+"\n\n\n")
    print("%d words" % self.get_rough_word_count())


  def maybe_change_character_emotions(self):
    npcs = [c for c in characters if c.is_player==False]
    for c in npcs:
      if random.random()<.2:
        if hasattr(c,"dispositions"): ## shouldn't need this unless error in characters.py
          c.change_disposition()


  def pickle_characters(self):
    """
    save character information 
    """
    with open(".characters_state_backup.pkl","wb") as f:
      f.write(pickle.dumps(self.characters))


  def save_question_state(self):
    """
    save current order of questions
    """
    with open('.questions.json','w') as f:
      json.dump(self.questions,f)


  def load_characters(self):
    """
    overwrites self.characters
    """
    with open(".characters_state_backup.pkl","rb") as f:
      self.characters = pickle.loads(f.read())


  def load_question_state(self):
    """
    overwrites self.questions
    """
    with open('.questions.json','r') as f:
      self.questions =json.load(f)


def main(reload):
  s = Salon(questions,characters,drinks.drinks2psycho)
  if reload==True: ## 
    input(colored("~~~WARNING:RELOADING SALON STATE~~~ENTER to continue", "red", attrs=["reverse", "blink"]))
    s.load_characters()
    s.load_question_state()
  elif reload==False:
    input(colored("~~~WARNING:NEW SALON~~~ENTER to continue", "green", attrs=["reverse", "blink"]))
  s.set_current_drinks()
  while True:
    s.new_dialogue()
    s.pickle_characters()
    s.save_question_state()
    s.maybe_change_character_emotions()
    print("~~~maybe adjust drinks?~~~")
    user_input = input("quit (q) or ENTER to continue>")
    if user_input == "q":
        print("~~~bye bye~~~")
        break
    s.set_current_drinks()


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--reload', type=str, default="") ## weirdly annoying to parse a bool, just using a string here
  args = parser.parse_args()
  reload = args.reload
  if reload.lower() == "yes": 
    main(reload=True)
  else:
    main(reload=False)