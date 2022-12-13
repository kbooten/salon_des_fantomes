import random
from copy import copy

import persons
all_characters = persons.get_people()

# from psychotropics.utterance_transformers.odd_parenthetical import add_odd_parenthetical
# from psychotropics.utterance_transformers.doubt import add_doubt
# from psychotropics.transformers import light_lucience
# from psychotropics.prompts import juan_crystalsmith


# starting_drinks = {key:val for key,val in drinks2psycho.items() if val==None} ## don't start with poison drink
# later_drinks = {key:val for key,val in drinks2psycho.items() if val!=None} ## don't start with poison drink



class DescriptionAdder:

    def __init__(self,characters,drinks):
        self.drink_prob = .2
        self.characters = characters
        self.prepared_text = ""
        self.drinks = drinks
        #self.set_drinks()
        self.set_character_drinks()


    def blood_test_text(self):
        text = "\n\n\n  *--[T O X I C O L O G Y  R E P O R T]*\n"
        for char in self.characters:
            text+="  *----%s:*\n" % char.name
            if len(char.psychotropics)==0:
                text+="  *-------within normal range*\n"
            else:
                for psy in char.psychotropics:
                    chem = self.drinks[psy]['chem']
                    permillion = int(self.drinks[psy]['prob'] * 10)
                    text+="  *-------%s: %d parts per million*\n" % (chem,permillion)
        return text

    def set_character_drinks(self):
        ## choose drink, maybe sticking with previous drink
        for char in self.characters:
            if char.beverage==None: ## 
                char.beverage = random.choice(list(self.drinks))
            else: 
                if random.random()<char.continue_drink_probability: ## possibly change drink
                    char.beverage = random.choice(list(self.drinks))
            print(char,char.beverage)

    def prepare_drink_statement(self,char,bev,psy=False,taste=None):
        text = "\n\n  **%s takes a sip of %s.**" % (char.name,bev)
        if psy==True:
            #text += "  **It tasted like %s.**\n" % random.choice(taste)
            # next_taste = drinks2psycho[bev]['cfg'].my_next() ## tick through the cfg
            next_taste = self.drinks[bev]['taste_func']()#()#.my_next()
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
        if self.drinks[bev]!=None: ### if has psychotropic character
            if bev not in char.psychotropics: ## first sip, add to dictionary
                char.psychotropics[bev] = copy(self.drinks[bev])
            else: ## keep sipping
                char.psychotropics[bev]["prob"]+=char.psychotropics[bev]["step"] ## increase by step
            #taste = drinks2psycho[bev]['taste']
            #self.prepare_drink_statement(char,bev,psy=True,taste=taste)
            self.prepare_drink_statement(char,bev,psy=True)
            if self.drinks[bev]['type']=="transform_character":
                self.drinks[bev]['function'](char) ## transform the character at each sip
        else:
            self.prepare_drink_statement(char,bev)

    def simple1(self,char):
        action = random.choice(['scratches','adjusts','idly taps','rubs'])
        body_part = random.choice(['wrist','skull','toe','index finger','chin','cheek','nose','left ass','right ass','lobes'])
        return "%s %s their %s." % (char,action,body_part)

    def simple2(self,char):
        action = random.choice(['adjusts','fondles','creases','brushes something off'])
        garb = random.choice(['beret','sash','glove','stole','gown','pants','scarf','hood','chain'])
        return "%s %s their %s." % (char,action,garb)

    def simple3(self,char):
        if random.random()<.4:
            action = random.choice(['yawns','leans forward','blinks','leans back','rocks agitatedly','snorts','smiles'])
        else:
            action = random.choice(['pulses','levitates up','levitates in','transmutates','beta-decays', 'colliderates','spalls','pionizes','urfshs','arcawints', 'eyo\'onts','yellowcakes out', 'map-merges', 'radixes', 'listens down'])

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

