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


from data import characters
chars = characters.characters

def get_ideas(loc):
    pref = "data/quotes_and_ideas/"
    with open(pref+loc,'r') as f:
        ideas = f.readlines()
    ideas = [i.rstrip("\n") for i in ideas]
    return ideas

def get_people():
    people = []
    player = Person("Kyle")
    player.is_player = True
    people.append(player)
    for c in chars.keys():
        person = Person(c)
        person.words = chars[c]['words']
        person.dispositions = chars[c]['dispositions']
        person.modes = chars[c]['modes']
        person.chattiness = chars[c]['chattiness']
        person.curiosity = chars[c]['curiosity']
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