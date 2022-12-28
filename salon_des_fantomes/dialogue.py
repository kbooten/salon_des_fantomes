import random,time,re

import gpt_interface

# import psytransform

import raw_dialogue_parsing as rdp

import fine_tuned_question_asker

from termcolor import colored, cprint

import json
with open('data/art/art_and_description.json','r') as f:
  artworks = json.load(f)


class Dialogue:


    def __init__(self,characters,question,description_adder):
        self.question = question
        self.description_adder = description_adder
        self.current_text = ""#prompt_prelude
        self.previous_thinker = None
        self.direct_question_asked = False
        self.first_statement_needed = True
        self.all_characters = characters
        self._get_start_char()
        self._start_prompt()
        self._create_start_question()
        self.initial_question_responded = False
        self.artworks = artworks.copy()
        random.shuffle(self.artworks)
        self.reader_question = False
        self.player = [c for c in characters if c.is_player][0]
        self.skipping_player=False


    def _get_start_char(self):
        try:
            self.current_thinker = [t for t in self.all_characters if t.name=="Socrates"][0]
        except:
            self.current_thinker = random.choice(self.all_characters)


    def _start_prompt(self):
        chars_string = ""
        last_character = self.all_characters[-1]
        for c in self.all_characters:
            if c!=last_character:
                chars_string+=c.name+", "
            else:
                chars_string+="and "+c.name
        p = "  **The philosophical salon continues. A group---%s---has gathered in one corner of the room, lounging on sofas.**" % chars_string
        p+="\n\n"
        self.current_text+=p


    def _create_start_question(self):
        question = 'Socrates: <My friends, I pose a question for our thoughtful discussion: %s>' % (self.question.strip())
        self.current_text += question

    def _next_thinker(self):
        """
        go back and forth between bots and player
        """
        if self.direct_question_asked==True:
            if random.random()<.7: ## usually return to previous bot
                self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker #swap
            else:
                thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
                thinker = random.choice(thinkers_available)
                self.previous_thinker = self.current_thinker
                self.current_thinker = thinker
        elif self.current_thinker.is_player==False: ## switch to human:
            self.current_thinker,self.previous_thinker = self.player,self.current_thinker
        else:
            if self.skipping_player==True: ## set only current thinker to new bot
                thinkers_available = [k for k in self.all_characters if (k!=self.current_thinker and k!=self.previous_thinker)]
                thinker = random.choice(thinkers_available)
                self.current_thinker = thinker
                self.skipping_player=False # reset
            else:
                if random.random()<.4:
                    ## sometimes return to the previous person to create continuity
                    self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker
                else:
                    thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
                    thinker = random.choice(thinkers_available)
                    self.previous_thinker = self.current_thinker
                    self.current_thinker = thinker


    def _refer_to_keyword_secret_prompt(self):
        print(colored('KEYWORD',"grey"))
        prefix = ""
        prompt_text = """

Write what <THINKER>, <LONGNAME>, would say next.  <MIN> words minimum, <MAX> words maximum of thoughtful, well-reasoned argument.  Even if the topic of the conversation is odd or silly, <THINKER> must take it silly.  End with punctuation and then the > symbol.  It should also possess a VERY <DISPOSITION> tone and should feature <STYLE>.  %s

<THINKER>: <<PREFIX>""" % random.choice(['Use the word or phrase "<KEYWORD1>".','Use the word or phrase "<KEYWORD1>" and the word or phrase "<KEYWORD2>".''Make sure to use the following words or phrases: "<KEYWORD1>", "<KEYWORD2>", and "<KEYWORD3>".'])
        if random.random()<self.current_thinker.chattiness:
            if random.random()<.3: 
                min,max = 250,500
            else:
                min,max = 150,250
        else:
            min,max = 50,150
        kw1,kw2,kw3 = self.current_thinker.get_unique_key_words(3)
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<KEYWORD1>",kw1)
        prompt_text = prompt_text.replace("<KEYWORD2>",kw2)
        prompt_text = prompt_text.replace("<KEYWORD3>",kw2)
        return {"prompt":prompt_text,"prefix":prefix}


    def _refer_back_to_question_secret_prompt(self):
        print(colored('BACK',"grey"))
        prefix = ""
        prompt_text = """

Write what <THINKER>, <LONGNAME>, would say next.  <MIN> words minimum, <MAX> words maximum of thoughtful, well-reasoned argument.  Even if the topic of the conversation is odd or silly, <THINKER> must take it silly.  End with punctuation and then the > symbol.  It should also possess a VERY <DISPOSITION> tone and should feature <STYLE>.  Connect back to the central question of the discussion, which is this: <QUESTION>

<THINKER>: <<PREFIX>"""
        if random.random()<self.current_thinker.chattiness:
            if random.random()<.3: 
                min,max = 250,500
            else:
                min,max = 150,250
        else:
            min,max = 50,150
        kw1,kw2,kw3 = self.current_thinker.get_unique_key_words(3)
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        return {"prompt":prompt_text,"prefix":prefix}


    def _mode_secret_prompt(self):
        print(colored('MODE',"grey"))
        prefix = ""
        prompt_text = """

Write what <THINKER>, <LONGNAME>, would say next.  <MIN> words minimum, <MAX> words maximum of thoughtful, well-reasoned argument.  Even if the topic of the conversation is odd or silly, <THINKER> must take it seriously.  End with punctuation and then the > symbol.  It should also possess a VERY <DISPOSITION> tone, feature <STYLE>.  It should try to <MODE>, making sure to do so in a way that connects to what <PREVIOUS_THINKER> just said.

<THINKER>: <<PREFIX>"""
        if random.random()<self.current_thinker.chattiness: 
            min,max = 300,500
        else:
            min,max = 100,300
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<MODE>",random.choice(self.current_thinker.modes))
        return {"prompt":prompt_text,"prefix":prefix}


    def _refer_to_quote_or_idea_secret_prompt(self):
        print(colored('QUOTE OR IDEA',"grey"))
        print(self.current_thinker.ideas)
        quote_or_idea = random.choice(self.current_thinker.ideas)
        ## build prompt
        prompt_text = """
Write what <THINKER>, <LONGNAME>, would say next.  <MIN> words minimum, <MAX> words maximum of thoughtful, well-reasoned argument.  Even if the topic of the conversation is odd or silly, <THINKER> must take it seriously.  End with punctuation and then the > symbol.  It should also possess a VERY <DISPOSITION> tone, feature <STYLE>.  It should try to <MODE>, making sure to do so in a way that connects to what <PREVIOUS_THINKER> just said.

<THINKER>: <<PREFIX>""" 

        if quote_or_idea.endswith('"'): # quote
          prefix = 'Allow me to connect this question we are discussing to something I once wrote: %s' % quote_or_idea
        else: ## idea
          prefix = "What you are saying reminds me a bit of the fact that %s" % quote_or_idea
        prompt_text = prompt_text.replace("<META>",meta_dialogue_instruction)
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<QUESTION>",self.question)    
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        return {"prompt":prompt_text,"prefix":prefix}

    def _consider_art_secret_prompt(self):
        print(colored('art','grey'))
        art = self.artworks.pop(0) ## take first
        self.artworks.append(art) ## and put on end
        artwork_title,artwork_description = art
        prefix = "What you are saying, %s, reminds me of this artwork above us, %s. In this" % (self.previous_thinker.name,art)
        prompt_text = """

Write ONLY the next utterance in the conversation by <THINKER>, <LONGNAME>, in response to the last statement by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
This response should be in the style of <THINKER>'s published writing. It should be <STYLE>. It should also possess a <DISPOSITION> tone and use the word or phrase <KEYWORD>.
This response should also reflect on the topic conversation in light of the famous artwork, <ART>.  Here is a description of the <ART>:

"<ART_DESCRIPTION>"


The next utterance you write should draw a clever, subtle connection between <ART> and what <PREVIOUS_THINKER> just said.

<THINKER>: <<PREFIX>""" 
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<ART>",artwork_title)
        prompt_text = prompt_text.replace("<ART_DESCRIPTION>",artwork_description)
        prompt_text = prompt_text.replace("<KEYWORD>",random.choice(self.current_thinker.words))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        return {"prompt":prompt_text,"prefix":prefix}

    def _ask_question_secret_prompt(self):
        print(colored('QUESTION',"grey"))
        if random.random()<.5:
            prefix = random.choice(
                ["My","That","Of","What","Clearly","Here","Let",
                "Please","Could you elaborate","Why","By what mechanism","How should"]
            )
        else:
            prefix = ""
        rhet_goals = [
        "raise a question about what <PREVIOUS_THINKER> means by a certain term",
        "put pressure on the argument that <PREVIOUS_THINKER> is making by coming up with a counterexample",
        "attack some implicit assumption of the argument that <PREVIOUS_THINKER> is making"
        ]
        prompt_text = """

Write ONLY a question that <THINKER>, <LONGNAME>, would ask in response to the last statement by by <PREVIOUS_THINKER>.
This question should be in the style of <THINKER>'s published writing. It should be <STYLE>. It should also possess a <DISPOSITION> tone.
This question should <RHETGOAL>.  50 to 100 words.

<THINKER>: <<PREFIX>""" 
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        prompt_text = prompt_text.replace("<RHETGOAL>",random.choice(rhet_goals)) ## must be first
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        return {"prompt":prompt_text,"prefix":prefix}

    def _ask_fine_tuned_question(self):
      last_utterance = rdp.excerpt_last_utterance(self.current_text)
      question = fine_tuned_question_asker.get_question_about_statement(last_utterance)
      return '\n\n%s: <%s>' % (self.current_thinker.name,question)


    def _generate_next_text(self):
        """
        the function that actually decides what kind of utterance is next.
        it is complicated. 

        firt it tries to do one of two things based on the state of the dialogue3
        -if Socrates has asked a question but not gotten a reply (as in the beginning of each dialogue), function will make current_thinker reply with default response
          -it may do this more than once
        - if a question has been asked, it will also force default response (so question can't follow question)

        otherwise it will do one of several things:
        - maybe ask a question
          - if it does, and the player is socrates, it will ask the fine tuned question
        - maybe refer to art
        - maybe refer to a specific idea from a person
        - default response

        """
        if self.direct_question_asked==True: ## if a question has been asked
            self.direct_question_asked=False ## switch off this need
            self.current_text += self._prompt2text(self._refer_to_keyword_secret_prompt()) ## standard response will do for response to questions
        else:
            if self.initial_question_responded==False:
                self.current_text+= self._prompt2text(self._refer_to_keyword_secret_prompt())
                self.initial_question_responded=True
            elif (random.random()<self.current_thinker.curiosity): ## QUESTION
                self.direct_question_asked = True # set variable so will know to return to questioned person
                if (random.random()<.3 and self.current_thinker.name=="Socrates"):
                    self.current_text += self._ask_fine_tuned_question() 
                else:
                    self.current_text+= self._prompt2text(self._ask_question_secret_prompt())
            elif (random.random()<.1 and self.current_thinker.ideas!=None): ## IDEA 
                self.current_text+= self._prompt2text(self._refer_to_quote_or_idea_secret_prompt())
            elif random.random()<.2:
                self.current_text+= self._prompt2text(self._mode_secret_prompt())
            elif random.random()<.9:
                self.current_text+= self._prompt2text(self._consider_art_secret_prompt())
            elif random.random()<.5:
                self.current_text+= self._prompt2text(self._refer_back_to_question_secret_prompt())
            else: ## how likely to just go with standard prompt
                self.current_text+= self._prompt2text(self._refer_to_keyword_secret_prompt())
        #self._possibly_elaborate()
        rdp.simple_regex_heal(self.current_text)


    def _prompt2text(self,prompt):
        """
        utility function that combines the prefix, gpt response, and end token
        """
        stub = '\n\n%s: <' % self.current_thinker.name
        if prompt["prefix"]!=None:
            stub+=prompt["prefix"]
        gpt_text = gpt_interface.gpt3_from_prompt(rdp.decomment_and_snip(self.current_text)+prompt['prompt'],max_tokens=500,stop=">")
        if gpt_text.endswith(">")==False:
            gpt_text = gpt_text + ">"
        return stub + gpt_text

    def either_human_or_bot(self):
        """
        this handles both human and bot turns
        """
        if (self.current_thinker.is_player==True):
            print(colored("human","yellow"))
            player_text = input("{}>")
            if player_text == "":
                self.skipping_player=True
            # elif player_text == "a":
            #     self._ask_fine_tuned_question()
            else:
                player_text = player_text.rstrip(" \n")
                self.current_text+='\n\n%s: <%s>' % (self.current_thinker.name,player_text)
                if player_text.endswith("?"):
                    self.direct_question_asked=True
        else:
            print(colored("bot","yellow"))
            self._generate_next_text()

    def _possibly_psychotrope(self):
        psychotropics = self.current_thinker.psychotropics
        random.shuffle(psychotropics)
        for psy in psychotropics:
            last_utterance = rdp.excerpt_last_utterance(self.current_text)
            if psy['type']=="transform_utterance": ## uses gpt
                transformed = psytransform.transform_text(last_utterance,self.current_thinker.psychotropics[psy]['function'],self.current_thinker.psychotropics[psy]['prob'])
                self.current_text = rdp.replace_last_instance(self.current_text,last_utterance,transformed)
            elif psy['type']=="transform_utterance_simple":
                transformed = psy.transform(transformed)
                self.current_text = rdp.replace_last_instance(self.current_text,last_utterance,transformed)


    def _possibly_describe(self):
        self.description_adder.possible_action()
        self.current_text+=self.description_adder.flush_text()


    def add_toxicology_report(self):
        self.current_text+=self.description_adder.blood_test_text()


    def next(self):
        print(colored(self.current_text,"red"))
        print(colored((self.previous_thinker.name if self.previous_thinker!=None else None ,self.current_thinker.name),'blue'))
        self._next_thinker()    ## change who is talking
        print(colored((self.previous_thinker.name if self.previous_thinker!=None else None ,self.current_thinker.name),'green'))
        #self.reader_question = False  ## has to go after _next_thinker, so maybe should be inside it?
        self.either_human_or_bot() ## generate the next line
        #self._possibly_psychotrope() ## maybe get weird
        self._possibly_describe() ## maybe add description of events
        # if self.initial_question_responded == False: ## just keep track of when first person has gone
        #   self.initial_question_responded = True ## in response to socrates, so he doesn't ask player question immediately
    

    def generate(self,n=10,toxicology_needed=True):
        for i in range(n):
            self.next()
            time.sleep(1)
        if self.direct_question_asked==True: ## don't end with question
            self.next()
        if toxicology_needed==True:
            self.add_toxicology_report()

