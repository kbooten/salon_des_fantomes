
import persons
characters = persons.get_people()

from data import questions
questions = questions.questions

from dialogue import Dialogue as dialogue

class Salon:

  def __init__(self,questions):
    self.questions = questions
    self.completed_dialogues = []

  def new_dialogue(self):
    next_question = self.questions.pop()
    current_dialogue = dialogue(characters,next_question)
    current_dialogue.generate()
    print(current_dialogue.current_text)
    self.make_memories(current_dialogue)
    self.completed_dialogues.append(current_dialogue)

  def make_memories(self,dialogue):
    print("need to make memories")

salon = Salon(questions)

def main():
  print(characters)
  print(questions)
  s = Salon(questions)
  s.new_dialogue()
  print(s.completed_dialogues[0])

if __name__ == '__main__':
  main()