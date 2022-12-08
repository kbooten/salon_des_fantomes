import persons
characters = persons.get_people()

from data import questions
questions = questions.questions

from dialogue import Dialogue
from description import DescriptionAdder,starting_drinks,later_drinks

import random

import time # for file naming

import dill as pickle


## using signal for timeout on user input
import signal
#
class AlarmException(Exception): # https://stackoverflow.com/q/27013127, https://stackoverflow.com/a/27014090, https://stackoverflow.com/a/494273
    pass
#
def signal_handler(signum, frame):
  raise AlarmException("user took to long")
#
signal.signal(signal.SIGALRM, signal_handler)


class Salon:

  def __init__(self,questions,characters):
    self.questions = questions
    #self.completed_dialogues = []
    self.characters = characters
    self.min_people = 4
    self.max_people = len(self.characters)
    ## saving output
    self.file_prefix = "output/output"
    self.output_file = self.get_file_name()
    ## adding drinks
    self.current_drinks = starting_drinks
    self.later_drinks = later_drinks
    self.chapter_number = 0

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
    next_question = self.questions.pop(0)
    self.questions.append(next_question)
    subset_of_characters = self.get_subset_of_characters()
    description_adder = DescriptionAdder(subset_of_characters,self.current_drinks)
    current_dialogue = Dialogue(characters,next_question,description_adder)
    current_dialogue.generate()
    print(current_dialogue.current_text)
    self.write_output("%d\n" % self.chapter_number)
    self.write_output(current_dialogue.current_text)
    self.write_output("\n\n\n")
    print("%d words" % self.get_rough_word_count())
    self.chapter_number+=1 ## tick up chapter number


  def maybe_add_psychotropic_drink(self):
    """
    add drink if enough words have been written
    """
    rough_word_count = self.get_rough_word_count()
    keys_to_delete = [] ## keep track of what is added
    for drink in self.later_drinks:
      if rough_word_count>self.later_drinks[drink]['after_wordcount']:
        self.current_drinks.update({drink:self.later_drinks[drink]})
        print("adding %s" % drink)
        print(self.current_drinks)
        keys_to_delete.append(drink)
    for del_drink in keys_to_delete: ## remove them from the list of addables
      del self.later_drinks[del_drink]

  def maybe_change_character_emotions(self):
    npcs = [c for c in characters if c.is_player==False]
    for c in npcs:
      if random.random()<.2:
        if hasattr(c,"dispositions"): ## shouldn't need this unless error in characters.py
          c.change_disposition()

  def try_to_pickle_characters(self):
    with open(".characters_state_backup.pkl","wb") as f:
      f.write(pickle.dumps(self.characters))


def main():
  s = Salon(questions,characters)
  while True:
    s.new_dialogue()
    s.maybe_add_psychotropic_drink()
    s.try_to_pickle_characters()
    # set signal to timeout
    signal.alarm(10)
    try:
      user_input = input("quit (q) or pause (p)>")
      if user_input=="p": # pause
        signal.alarm(0)
        input("paused. hit ENTER to keep going.")
      elif user_input == "q":
        print("quitting")
        break
    except:
      signal.alarm(0)
      pass
    s.maybe_change_character_emotions()

    

if __name__ == '__main__':
  main()