import persons
characters = persons.get_people()

from data import questions
questions = questions.questions

from dialogue import Dialogue
from description import DescriptionAdder

import random

import time # for file naming


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

  def get_file_name(self):
    y,mo,d,h,min = time.localtime()[:5] # 
    return "%s_%d-%d-%d_%d~%d.txt" % (self.file_prefix,mo,d,y,h,min)

  def get_rough_word_count(self):
    with open(self.output_file,'r') as f:
      text = f.read()
    tokens = text.split(' ')
    words = [t for t in tokens if any(c.isalpha() for c in t)]
    return len(words)


  def get_subset_of_characters(self):
    mandatory = [char for char in characters if (char.is_player==True or char.name=="Socrates")]
    other_possibilities = [char for char in characters if char not in mandatory] ## all other possibilities
    n_to_select = random.randrange(self.min_people,self.max_people) - len(mandatory)
    others_chosen = random.sample(other_possibilities,n_to_select)
    subset_of_characters = others_chosen+mandatory
    return subset_of_characters

  def write_output(self,text):
    try: ## adding to file
      f = open(self.output_file,'a')
      print('writing to %s' % self.output_file)
    except FileNotFoundError: ## new file
      print('creating %s' % self.output_file)
      f = open(self.output_file,'w')
    f.write(text)
    f.close()

  def new_dialogue(self):
    next_question = self.questions.pop()
    subset_of_characters = self.get_subset_of_characters()
    description_adder = DescriptionAdder(subset_of_characters)
    current_dialogue = Dialogue(characters,next_question,description_adder)
    current_dialogue.generate()
    print(current_dialogue.current_text)
    self.write_output(current_dialogue.current_text)
    print("%d words" % self.get_rough_word_count())

def main():
  while True:
    s = Salon(questions,characters)
    s.new_dialogue()
    # set signal to timeout
    signal.alarm(10)
    try:
      if input("to quit enter 'quit'>")=="quit":
        break
    except:
      signal.alarm(0)
      pass
    

if __name__ == '__main__':
  main()