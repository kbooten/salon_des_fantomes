import random,time,re

import gpt_interface

import psytransform

import raw_dialogue_parsing as rdp

import fine_tuned_question_asker

from termcolor import colored

import json
with open('data/art/art_and_description.json','r') as f:
  artworks = json.load(f)
random.shuffle(artworks)


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
        self.since_player_spoke = 0
        self.meta = "Write what <THINKER> would say in reply to what <PREVIOUS_THINKER> has said.  <THINKER> is <LONGNAME>.  <MIN> words minimum, <MAX> words maximum of thoughtful, well-reasoned, detailed and information-filled argument. What <THINKER> says next should build on what <PREVIOUS_THINKER> has just said, and it should should not contradict what <THINKER> has said previously. Even if the topic of the conversation is odd or silly, <THINKER> must take it seriously and must not object to or evade the topic of conversation or disagree with the premise.  <THINKER>'s next utterance must not give a wishy-washy answer (like 'well, it depends' or 'sometimes yes, sometimes no' or 'both have their merits'---or any other wishy-washy, moderate opinion); if asked to choose between something or imagine something, <THINKER> must make a bold choice.  <THINKER> must say something EXTREME, not something moderate. What <THINKER> says next should use a <DISPOSITION> tone and should feature <STYLE> and a strong, intense, weird, and interesting opinion that a normal person is not likely to have. End with punctuation and then the > symbol."
        self.player_spoken_enough = False
        self.desired_char_length_for_player_input = 400 ## must be at least one player input of this many characters
        self.kill_dialogue=False

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
            if random.random()<.7: ## usually return to previous person
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
                else: ## randomly choose next person
                    thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
                    thinker = random.choice(thinkers_available)
                    self.previous_thinker = self.current_thinker
                    self.current_thinker = thinker


    def _refer_to_keyword_secret_prompt(self):
        """
        respond using one or more keywords
        """
        print(colored('KEYWORD',"grey"))
        prefix = ""
        prompt_text = """
        
<META>
<KEYWORD_COMMAND>

<THINKER>: <<PREFIX>"""
        if random.random()<.12:
            keyword_command = "" ## no keyword actually...
            min,max = 70,200
        elif random.random()<.9:
            keyword_command = 'Use the word or phrase "<KEYWORD1>".'
            min,max = 150,400
        else:
            keyword_command = 'Use the word or phrase "<KEYWORD1>" and the word or phrase "<KEYWORD2>".'
            min,max = 350,500
        prompt_text = prompt_text.replace("<KEYWORD_COMMAND>",keyword_command)
        kw1,kw2 = self.current_thinker.get_unique_key_words(2)
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<KEYWORD1>",kw1)
        prompt_text = prompt_text.replace("<KEYWORD2>",kw2)
        prompt_text = prompt_text.replace("<KEYWORD_COMMAND>",keyword_command)
        return {"prompt":prompt_text,"prefix":prefix}


    def _refer_back_to_question_secret_prompt(self):
        """
        bring the conversation back to the question
        """
        print(colored('BACK',"grey"))
        prefix = ""
        prompt_text = """

<META>
What <THINKER> says next should connect the conversation back to the central question which began it: <QUESTION>

<THINKER>: <<PREFIX>"""
        if random.random()<self.current_thinker.chattiness:
            if random.random()<.3: 
                min,max = 200,300
            else:
                min,max = 100,200
        else:
            min,max = 50,100
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<QUESTION>",self.question)
        return {"prompt":prompt_text,"prefix":prefix}


    def _mode_secret_prompt(self):
        """
        make use of a character's mode attribute
        """
        print(colored('MODE',"grey"))
        prefix = ""
        prompt_text = """

<META>
<THINKER>'s next line should try to <MODE>.  Make sure to do so in a way that connects to what <PREVIOUS_THINKER> just said.

<THINKER>: <<PREFIX>"""
        if random.random()<self.current_thinker.chattiness: 
            min,max = 300,500
        else:
            min,max = 100,300
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(min))
        prompt_text = prompt_text.replace("<MAX>",str(max))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<MODE>",random.choice(self.current_thinker.modes))
        return {"prompt":prompt_text,"prefix":prefix}


    def _refer_to_quote_or_idea_secret_prompt(self):
        """
        make use of a character's quote/idea
        """
        print(colored('QUOTE OR IDEA',"grey"))
        quote_or_idea = random.choice(self.current_thinker.ideas)
        ## build prompt
        prompt_text = """

<META>

<THINKER>: <<PREFIX>""" 

        if quote_or_idea.endswith('"'): # quote
          prefix = 'Allow me to connect this question we are discussing to something I once wrote: %s' % quote_or_idea
        else: ## idea
          prefix = "What you are saying reminds me, if obliquely, of the fact that %s" % quote_or_idea
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(200))
        prompt_text = prompt_text.replace("<MAX>",str(500))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        return {"prompt":prompt_text,"prefix":prefix}


    def _agree_secret_prompt(self):
        """
        agree with previous character
        """
        print(colored('AGREE','grey'))
        prefix = random.choice([
                "I think I know what you are saying.",
                "Let me try to put your idea a little differently:",
                "Right,",
                "Exactly, and this is why",
                "Let's say that you are correct:",
                "This would explain",
                "I take your point."
            ])
        prompt_text = """

<META>
The next utterance should essentially agree with what <PREVIOUS_THINKER> just said, though it should also add something to it, refracting it in to the point of view of <THINKER>.

<THINKER>: <<PREFIX>""" 
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(20))
        prompt_text = prompt_text.replace("<MAX>",str(140))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        return {"prompt":prompt_text,"prefix":prefix}


    def _consider_art_secret_prompt(self):
        """
        comment on a piece of art
        """
        print(colored('ART','grey'))
        art = self.artworks.pop(0) ## take first
        self.artworks.append(art) ## and put on end
        artwork_title,artwork_description = art
        prefix = "What you are saying, %s, reminds me of this artwork above us, %s. In this" % (self.previous_thinker.name,artwork_title)
        prompt_text = """

<META>
This response should also reflect on the topic conversation in light of the famous artwork, <ART>.  Don't invent details of <ART> that aren't in this description:

"<ART_DESCRIPTION>"

The next utterance you write should draw a clever, subtle connection between <ART> and what <PREVIOUS_THINKER> just said, mentioning specific details of the art.

<THINKER>: <<PREFIX>""" 
        prompt_text = prompt_text.replace("<META>",self.meta)
        prompt_text = prompt_text.replace("<MIN>",str(200))
        prompt_text = prompt_text.replace("<MAX>",str(500))
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
        prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
        prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
        prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
        prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
        prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
        prompt_text = prompt_text.replace("<PREFIX>",prefix)
        prompt_text = prompt_text.replace("<ART>",artwork_title)
        prompt_text = prompt_text.replace("<ART_DESCRIPTION>",artwork_description)
        return {"prompt":prompt_text,"prefix":prefix}


    def _ask_question_secret_prompt(self):
        """
        ask a question
        """
        print(colored('QUESTION',"grey"))
        if random.random()<.5:
            prefix = random.choice(
                ["My","That","What","Here","So",
                "Please","Could you","Why","How do","How","Why","But","But","How should"]+[""]*10
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
        prompt_text = prompt_text.replace("<PREVIOUS>",rdp.decomment_and_snip(self.current_text))
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
            self.direct_question_asked=False ## switch off this need so don't keep asking questions
            next_utterance = self._prompt2text(self._refer_to_keyword_secret_prompt()) ## standard response will do for response to questions
        else:
            if self.initial_question_responded==False: ## if nobody responded to socrates
                next_utterance = self._prompt2text(self._refer_to_keyword_secret_prompt()) ## just do normal response
                self.initial_question_responded=True 
            elif (random.random()<self.current_thinker.curiosity): ## QUESTION
                self.direct_question_asked = True # set variable so will know to return to questioned person, though this may be redundant since I also check the string for "?"
                if (random.random()<.3 and self.current_thinker.name=="Socrates"):
                    next_utterance = self._ask_fine_tuned_question() ## my special question model
                else:
                    next_utterance = self._prompt2text(self._ask_question_secret_prompt())
            elif (random.random()<.5 and random.random()<self.current_thinker.agreeability): ## AGREE, agree sometimes
                next_utterance = self._prompt2text(self._agree_secret_prompt())
            elif (random.random()<.12 and self.current_thinker.ideas!=None): ## IDEA, some may not have them
                next_utterance = self._prompt2text(self._refer_to_quote_or_idea_secret_prompt())
            elif random.random()<.3:
                next_utterance = self._prompt2text(self._mode_secret_prompt()) ## MODE
            elif random.random()<.2:
                next_utterance = self._prompt2text(self._consider_art_secret_prompt()) ## ART
            elif random.random()<.25:
                next_utterance = self._prompt2text(self._refer_back_to_question_secret_prompt()) ## REFER BACK
            else: ## how likely to just go with standard prompt
                next_utterance = self._prompt2text(self._refer_to_keyword_secret_prompt())
        next_utterance = rdp.simple_regex_heal(next_utterance) ## handle outputs that aren't quite right
        if "?" in next_utterance: ## check for question:
            self.direct_question_asked = True
        self.current_text+=next_utterance


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


    def get_specific_question_for_player(self):
        """
        special questions for player
        """
        qs = [
        "What do you think, %s?",
        "How might we dispute this, %s?",
        "Could you support this argument, %s?",
        ]
        if random.random()<.3:
            qs += [
            "I wonder if you might provide a historical detail to support this argument, %s?",
            "I wonder if you might provide some scientific argument, %s?",
            "What other facts would one need in order to find this argument credible, %s?",
            "%s, I believe there was a study published recently that relates to this point.  Would you mind trying to find it?",
            "Can you connect this more firmly to the question that began this conversation, %s?"
            ]
        question = "\n  **Socrates: %s**" % random.choice(qs) 
        question = question % self.player.name
        return question


    def either_human_or_bot(self):
        """
        this handles both human and bot turns
        """
        player_text = ""
        if (self.current_thinker.is_player==True):
            print(colored(self.current_text,"blue"))
            if self.since_player_spoke>2 and random.random()<.4: ## mandatory
                specific_question = self.get_specific_question_for_player()
                self.current_text+=specific_question
                print(colored(specific_question,"blue"))
                while len(player_text)<self.desired_char_length_for_player_input:
                    player_text = input("{🛑}>")
                    if len(player_text)<self.desired_char_length_for_player_input:
                        print("(response not long enough; add more characters)")
            else: ### non mandatory
                player_text = input("{🔶}>")
            if player_text.lower()=="kill": ## escape hatch
                player_text = ""
                self.kill_dialogue=True
            if player_text=="":
                self.skipping_player = True
                self.since_player_spoke+=1
            else:
                if len(player_text)>self.desired_char_length_for_player_input: ## mandatory n character response
                    self.player_spoken_enough = True
                self.since_player_spoke=0 ## reset
                player_text = player_text.rstrip(" \n")
                self.current_text+='\n\n%s: <%s>' % (self.current_thinker.name,player_text)
                if "?" in player_text:
                    self.direct_question_asked=True
                self.since_player_spoke = 0 ## reset counter
        else:
            self._generate_next_text()


    def _possibly_psychotrope(self):
        psychotropics = self.current_thinker.psychotropics#[psy for psy in self.current_thinker.psychotropics if psychotropics[psy]['type']=="transform_utterance"]
        psychotropics_keys = [drink for drink in psychotropics if psychotropics[drink]['type']=="transform_utterance"]
        random.shuffle(psychotropics_keys)
        for psy in psychotropics_keys:
            last_utterance = rdp.excerpt_last_utterance(self.current_text)
            transformed = psytransform.transform_text(last_utterance,psychotropics[psy]['function'].prompt,psychotropics[psy]['prob'])
            self.current_text = rdp.replace_last_instance(self.current_text,last_utterance,transformed)


    def _possibly_describe(self):
        self.description_adder.possible_action()
        self.current_text+=self.description_adder.flush_text()


    def add_toxicology_report(self):
        self.current_text+=self.description_adder.blood_test_text()


    def next(self):
        time.sleep(1)
        self._next_thinker()    ## change who is talking
        self.either_human_or_bot() ## generate the next line
        self._possibly_psychotrope() ## maybe get weird
        self._possibly_describe() ## maybe add description of events
    

    def generate(self,n=10,toxicology_needed=True):
        for i in range(n):
            self.next()
            print("\nroughly %s words" % len(self.current_text.split()))
            if self.kill_dialogue==True:
                break
        ## wrapping up
        input("wrapping up")
        while (self.direct_question_asked==True or self.player_spoken_enough==False): ## don't end with question or until player has spoken enough
            self.next()
        if toxicology_needed==True:
            self.add_toxicology_report()
        print(colored(self.current_text,"blue"))
        print("")

