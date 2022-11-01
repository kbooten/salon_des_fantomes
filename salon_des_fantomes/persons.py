class Person:

  def __init__(self,name):
    self.name = name
    words = []
    memories = []

  def __repr__(self):
    return "%s(%s)" % (self.__class__,self.name)


from data import characters
chars = characters.characters

def get_people():
    people = []
    for c in chars.keys():
        person = Person(c)
        person.words = chars[c]['words']
        person.dispositions = chars[c]['dispositions']
        person.modes = chars[c]['modes']
        person.chattiness = chars[c]['chattiness']
        person.curiosity = chars[c]['curiosity']
        people.append(person)
    return people

def main():
    people = get_people()
    print(people)

if __name__ == '__main__':
    main()