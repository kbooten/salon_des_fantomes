import random
from copy import copy

import persons
all_characters = persons.get_people()

from psychotropics.odd_parenthetical import add_odd_parenthetical
from psychotropics.doubt import add_doubt

from cfgs import *

drinks2psycho = {
    "water":None,
    "port":None,
    "calvados":None,
    "chablis":None,
    "sherry":None,
    "amontillado":None,
    "madeira":None,
    "dry vermouth":None,
    "sweet vermouth":None,
    "scotch":None,
    "brandy":None,
    "1961 Pétrus":{
                    "function":add_odd_parenthetical,
                    #"taste":["like a muddy mixtape","like a few highlighters","like a bismuth spoon","like a signal splitter"],
                    "prob":0.9,
                    "step":0.02,
                    "cfg":cfg2,
                    "chem":"bisephontinol-3",
                    'after_wordcount':1,#0000,
                    },
    "1950 Château Lafleur":{
                    "function":add_doubt,
                    #"taste":["like rabbit breath","like leather water","rainy","like a memory of chalk","like a perfect ravine"],
                    "prob":0.9,
                    "step":0.3,
                    "cfg":cfg1,
                    "chem":"3-hydroxaform-butane",
                    'after_wordcount':1,#30000,
                    },
}


starting_drinks = {key:val for key,val in drinks2psycho.items() if val==None} ## don't start with poison drink
later_drinks = {key:val for key,val in drinks2psycho.items() if val!=None} ## don't start with poison drink


class DescriptionAdder:

    def __init__(self,characters,possible_drinks):
        self.drink_prob = .2
        self.possible_statement = ""
        self.characters = characters
        self.prepared_text = ""
        self.possible_drinks = possible_drinks
        self.set_character_drinks()

    def blood_test_text(self):
        text = "\n\n\n  *--[T O X I C O L O G Y  R E P O R T]*\n"
        for char in self.characters:
            text+="  *----%s:*\n" % char.name
            if len(char.psychotropics)==0:
                text+="  *-------within normal range*\n"
            else:
                for psy in char.psychotropics:
                    chem = drinks2psycho[psy]['chem']
                    permillion = int(drinks2psycho[psy]['prob'] * 10)
                    text+="  *-------%s: %d parts per million*\n" % (chem,permillion)
        return text

    def set_character_drinks(self):
        ## choose drink, maybe sticking with previous drink
        for char in self.characters:
            if char.beverage==None: ## 
                char.beverage = random.choice(list(self.possible_drinks))
            else: 
                if random.random()<char.continue_drink_probability: ## possibly change drink
                    char.beverage = random.choice(list(drinks2psycho))
            print(char,char.beverage)

    def prepare_drink_statement(self,char,bev,psy=False,taste=None):
        text = "\n\n  **%s takes a sip of %s.**" % (char.name,bev)
        if psy==True:
            #text += "  **It tasted like %s.**\n" % random.choice(taste)
            next_taste = drinks2psycho[bev]['cfg'].my_next() ## tick through the cfg
            text += "\n  **It tastes like %s.**" % next_taste#random.choice(taste)
            if random.random()<.23:
                text += "\n"+random.choice([
                                    "  **Was it supposed to taste like this?**",
                                    "  **And it was cloudy.**",
                                    "  **An unfamiliar pulse in the cerebelum.**",
                                    "  **A flicker of nausea, easy to ignore.**",
                                    "  **Immediate lightheadedness. Not entirely pleasant.**"])+"\n"
        self.prepared_text += text ### adds text

    def make_character_drink(self,char):
        bev = char.beverage
        print(">>")
        print(char,bev)
        print("<<")
        if drinks2psycho[bev]!=None: ### if has psychotropic character
            if bev not in char.psychotropics: ## first sip, add to dictionary
                char.psychotropics[bev] = copy(drinks2psycho[bev])
            else: ## keep sipping
                char.psychotropics[bev]["prob"]+=char.psychotropics[bev]["step"] ## increase by step
            #taste = drinks2psycho[bev]['taste']
            #self.prepare_drink_statement(char,bev,psy=True,taste=taste)
            self.prepare_drink_statement(char,bev,psy=True)
        else:
            self.prepare_drink_statement(char,bev)

    def simple1(self,char):
        action = random.choice(['scratches','adjusts','idly taps','rubs'])
        body_part = random.choice(['wrist','skull','toe','index finger','chin','cheek','nose','left ass','right ass'])
        return "%s %s their %s." % (char,action,body_part)

    def simple2(self,char):
        action = random.choice(['adjusts','fondles','creases','brushes something of'])
        garb = random.choice(['beret','sash','glove','stole','gown'])
        return "%s %s their %s." % (char,action,garb)

    def simple3(self,char):
        action = random.choice(['yawns','leans forward','blinks','leans back','rocks agitatedly'])
        return "%s %s." % (char,action)

    def simple_description(self):
        c = 0
        chars = [c.name for c in self.characters]
        random.shuffle(chars)
        for char in chars:
            if random.random()<.2:
                simplefunc = random.choice([
                        self.simple1,
                        self.simple2,
                        self.simple3
                    ])
                self.prepared_text+="\n\n  **%s**\n" % simplefunc(char)


    def flush_text(self):
        text = str(self.prepared_text)
        self.prepared_text = ""
        return text

    def possible_action(self):
        char = random.choice(self.characters)
        if random.random()<self.drink_prob:
            self.make_character_drink(char)
        else:
            self.simple_description()    

def main():
    d = DescriptionAdder(all_characters,drinks2psycho)
    for i in range(100):
        d.possible_action()
        print(d.flush_text())
    print(d.blood_test_text())


if __name__ == '__main__':
  main()

