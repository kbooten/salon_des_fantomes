import random

class Person:

  def __init__(self,name):
    self.name = name
    self.is_player = False
    self.beverage = None
    self.psychotropics = {
            ##"function"
        }
    self.continue_drink_probability = random.random()
    self.ideas = None

  def __repr__(self):
    return "%s(%s)" % (self.__class__,self.name)

  def change_disposition(self):
    popped_dis = self.dispositions.pop(0)
    self.dispositions.append(popped_dis) ## back of line
    self.current_disposition = self.dispositions[0] ## new zeroeth

from data import characters
chars = characters.characters

def get_ideas(loc):
    pref = "data/quotes_and_ideas/"
    with open(pref+loc,'r') as f:
        ideas = f.readlines()
    ideas = [i.rstrip("\n") for i in ideas]
    ideas = [i for i in ideas if len(i)>0] ## in case extra lines 
    return ideas

def get_sample_texts(loc):
    pref = "data/example_prose/"
    with open(pref+loc,'r') as f:
        rawtext = f.read()
    paragraphs = [i for i in x.split("\n\n") if len(i)>3]
    paragraphs = [i.replace("\n"," ").rstrip(" ") for i in paragraphs]
    paragraphs = [i.replace("-  ","") for i in paragraphs]
    return paragraphs

def get_people():
    people = []
    for c in chars.keys():
        person = Person(c)
        if c=="Kyle":
            person.is_player=True
        person.longname = chars[c]['longname']
        person.words = chars[c]['words']
        person.dispositions = chars[c]['dispositions']
        #person.current_disposition = person.dispositions[0]
        person.modes = chars[c]['modes']
        person.chattiness = chars[c]['chattiness']
        person.curiosity = chars[c]['curiosity']
        person.style = chars[c]['style']
        if "quotes" in chars[c]:
            person.ideas = get_ideas(chars[c]['quotes'])
        people.append(person)
    return people

def main():
    people = get_people()
    print(people)
    for p in people:
        print(p.ideas)

if __name__ == '__main__':
    main()