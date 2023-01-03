import random
from copy import copy
import re

import persons
all_characters = persons.get_people()

class DescriptionAdder:

    def __init__(self,characters,drinks):
        self.drink_prob = .6
        self.simple_description_prob = .2
        self.characters = characters
        self.prepared_text = ""
        self.drinks = drinks
        self.set_character_drinks()


    def blood_test_text(self):
        text = "\n\n\n  *--[T O X I C O L O G Y  R E P O R T]*\n"
        for char in self.characters:
            text+="  *----%s:*\n" % char.name
            if len(char.psychotropics)==0:
                text+="  *-------within normal range*\n"
            else:
                for psy in char.psychotropics:
                    chem = self.drinks[psy]['function']
                    permillion = int(self.drinks[psy]['prob'] * 10)
                    chemline = "  *-------%s: %d ppm*\n" % (chem,permillion)
                    text+=chemline
        return text


    def set_character_drinks(self):
        ## choose drink, maybe sticking with previous drink
        for char in self.characters:
            if (char.is_player==True or char.name=="Socrates"):
                char.beverage = random.choice([bev for bev in self.drinks if self.drinks[bev]==None]) ## player always drinks something non-psycho
            elif char.beverage==None: ## 
                char.beverage = random.choice(list(self.drinks))
            else: 
                if random.random()<char.curiosity: ## possibly change drink
                    char.beverage = random.choice(list(self.drinks))


    def prepare_drink_statement(self,char,bev,psy=False,taste=None):
        text = "\n\n  **%s takes a sip of %s.**" % (char.name,bev)
        if psy==True:
            if random.random()<.23:
                text += "\n"+random.choice([
                                    "  **Was it supposed to taste like this?**",
                                    "  **And sore turbid it was.**",
                                    "  **An unfamiliar pinching in the cerebelum.**",
                                    "  **A micropump of nausea, easy to ignore.**",
                                    "  **Immediate leftheadedness. Not entirely pleasant.**"])+"\n"
        self.prepared_text += text ### adds text


    def make_character_drink(self,char):
        bev = char.beverage
        if self.drinks[bev]!=None: ### if has psychotropic character
            ## add to dictionary
            if bev not in char.psychotropics: ## first sip, add to dictionary
                char.psychotropics[bev] = copy(self.drinks[bev])
                self.prepare_drink_statement(char,bev,psy=True)
            ## either use now or save for later
            if self.drinks[bev]["type"]=="transform_utterance":
                self.prepare_drink_statement(char,bev,psy=True)
                char.psychotropics[bev]["prob"]+=char.psychotropics[bev]["step"] ## increase by step
            elif self.drinks[bev]['type']=="transform_character_words":
                char.words.append(self.drinks[bev]['function']())
            elif self.drinks[bev]['type']=="transform_character_modes":
                char.modes.append(self.drinks[bev]['function']())
            elif self.drinks[bev]['type']=="transform_character_dispositions":
                char.dispositions.append(self.drinks[bev]['function']())
        else:
            self.prepare_drink_statement(char,bev)


    def simple1(self,char):
        action = random.choice(['scratches','adjusts','idly taps','rubs'])
        body_part = random.choice(['wrist','skull','toe','index finger','chin','cheek','nose','left ass','right ass','lobes'])
        return "%s %s their %s." % (char,action,body_part)


    def simple2(self,char):
        action = random.choice(['adjusts','fondles','creases','brushes something off'])
        if random.random()<.95:
            garb = random.choice(['sash','glove','gown','pants','pants','pants','shirt','coat','scarf','cloak','hood','vest','sleeve','sleeve','collar'])
        else:
            garb =  random.choice(['chain','snood','wimple','cravat','khimar','cilice','carapace','rekel','alb','surcingle','antarvāsa','uttarāsaṅga'])
        return "%s %s their %s." % (char,action,garb)


    def simple3(self,char):
        if random.random()<.95:
            action = random.choice(['yawns','leans forward','blinks','leans back','rocks agitatedly','snorts','smiles'])
        else:
            action = random.choice(['pulses','levitates up','levitates in','transmutates','beta-decays', 'colliderates','spalls','pionizes','urfshs','arcawints', 'eyo\'onts','yellowcakes out', 'map-merges', 'radixes', 'listens down'])

        return "%s %s." % (char,action)


    def simple_description(self,char):
        simplefunc = random.choice([
                self.simple1,
                self.simple2,
                self.simple3
            ])
        self.prepared_text+="\n\n  **%s**\n" % simplefunc(char.name)


    def flush_text(self):
        text = str(self.prepared_text)
        self.prepared_text = ""
        return text

    def possible_action(self):
        char = random.choice(self.characters)
        if random.random()<self.drink_prob:
            self.make_character_drink(char)
        elif random.random()<self.simple_description_prob:
            self.simple_description(char)    

def main():
    d = DescriptionAdder(all_characters,drinks2psycho)
    for i in range(100):
        d.possible_action()
        print(d.flush_text())
    print(d.blood_test_text())


if __name__ == '__main__':
  main()

