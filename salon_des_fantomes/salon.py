import persons
characters = persons.get_people()

from data import questions
questions = questions.questions

from dialogue import Dialogue
from description import DescriptionAdder


class Salon:

  def __init__(self,questions):
    self.questions = questions
    self.completed_dialogues = []

  def new_dialogue(self):
    next_question = self.questions.pop()
    description_adder = DescriptionAdder(characters)
    current_dialogue = Dialogue(characters,next_question,description_adder)
    current_dialogue.generate()
    print(current_dialogue.current_text)
    self.completed_dialogues.append(current_dialogue) ## not just text?

salon = Salon(questions)

def main():
  print(characters)
  print(questions)
  s = Salon(questions)
  s.new_dialogue()
  print(s.completed_dialogues[0])

if __name__ == '__main__':
  main()