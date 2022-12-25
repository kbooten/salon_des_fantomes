import random,time,re

import gpt_interface

import psytransform

import raw_dialogue_parsing as rdp

import fine_tuned_question_asker

with open('data/art.txt','r') as f:
  artworks = [a.rstrip("\n") for a in f.readlines()]

from ask_player_questions import QuestionAsker

from termcolor import colored, cprint


meta_dialogue_instruction = """

You are writing a script for a philosophical dialogue in which one person talks and then another talks.  Lines of dialogue are between < and > characters, like this:


Socrates: <Then, my friend, we must not regard what the many say of us; but what he, the one man who has understanding of just and unjust, will say, and what the truth will say. And therefore you begin in error when you advise that we should regard the opinion of the many about just and unjust, good and evil, honourable and dishonourable.—'Well,' someone will say, 'but the many can kill us.'>

Crito: <Yes, Socrates; that will clearly be the answer.  And I will search for the answer.>

Socrates: <And it is true; but still I find with surprise that the old argument is unshaken as ever. And I should like to know whether I may say the same of another proposition—that not life, but a good life, is to be chiefly valued?>


"""


class Dialogue:


  def __init__(self,characters,question,description_adder):
    self.question = question
    self.description_adder = description_adder
    self.temperature=0.9
    self.max_tokens=70
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
    self.qa = QuestionAsker(self.player)
    self.interrupt = False
    self.interrupt_text = ""


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
    question = '%s: <My friends, I pose a question for our thoughtful discussion: %s>' % (self.current_thinker.name,self.question.strip())
    self.current_text += question


  def _next_thinker(self):
    if (self.current_thinker!=self.player and self.direct_question_asked==False):
      interrupt = input("{interrupt?}>")
      if interrupt!="":
        self.interrupt=True
        self.previous_thinker = self.current_thinker
        self.current_thinker = self.player
        self.interrupt_text = interrupt
        return
    if self.direct_question_asked==True: ## question has been asked, need to return to it
      self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker #swap
    elif self.initial_question_responded == False: 
        ## don't allow player to respond first
        ## because this would cause socrates to follow socrates, since socrates always asks player question 
        thinkers_available = [k for k in self.all_characters if (k!=self.current_thinker and k.is_player==False)]
        thinker = random.choice(thinkers_available)
        self.previous_thinker = self.current_thinker
        self.current_thinker = thinker
    else:
      # ## if player is the previous_person, maybe return to them (i.e. focus on player, create player/nonplayer loops)
      # if (self.current_thinker.is_player==False and self.previous_thinker.is_player==False and self.reader_question==False):
      #   if random.random()<.3:
      #     self.previous_thinker = self.current_thinker
      #     self.current_thinker = self.player
      # else:
        ## just randomly go to someone else next
      thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
      ## change the thinker, but save previous
      thinker = random.choice(thinkers_available)
      self.previous_thinker = self.current_thinker
      self.current_thinker = thinker

  def _refer_to_keyword_secret_prompt(self):
    print('main')
    prefix = ""
    prompt_text = """

    <META>

    ***

    Here is part of a script that we are working on, a conversation between some people.

    <PREVIOUS>

    ***

    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by <PREVIOUS_THINKER>.
    This utterance should obey the following rules perfecty:
    1. Important!: It should give detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    2. Important!: It should be in the style of <THINKER>'s published writing.
    3. Important!: It should also possess a VERY <DISPOSITION> tone and should feature <STYLE>.
    5. Important!: It should include the word <KEYWORD> in the first one or two sentences. 
    6. Important!: It should not repeat itself OR ANY PREVIOUS SENTENCES UTTERED BY THIS OR OTHER CHARACTERS. Each sentence should offer a new idea.
    7. Important!: 100-300 words.
    8. Important!: It should express a strange, counter-intuitive opinion that is charateristic of <THINKER> uniquely, not a general one that many people might hold.

    Ok, now complete the dialogue, ending with punctuation and then the > symbol.

    <THINKER>: <<PREFIX>""" 
    prompt_text = prompt_text.replace("<META>",meta_dialogue_instruction)
    prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
    prompt_text = prompt_text.replace("<QUESTION>",self.question)
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
    prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
    prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
    prompt_text = prompt_text.replace("<PREFIX>",prefix)
    prompt_text = prompt_text.replace("<KEYWORD>",random.choice(self.current_thinker.words))
    return {"prompt":prompt_text,"prefix":prefix}


  def _refer_to_quote_or_idea_secret_prompt(self):
    print('refer to quoteidea')
    print(self.current_thinker.ideas)
    quote_or_idea = random.choice(self.current_thinker.ideas)
    ## build prompt
    prompt_text = """

    <META>

    ***

    Here is part of a script that we are working on, a conversation between some people.

    <PREVIOUS>

    ***

    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    <THINKER> is <LONGNAME>.
    This response should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone. 

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


  def _ask_question_secret_prompt(self):
    print('question')
    if random.random()<.5:
      prefix = random.choice(
        ["My","That","Of","What","Clearly","Here","Let",
        "Please","Could you elaborate","Why","By what mechanism","How should"]
        )
    else:
      prefix = ""
    rhet_goals = [
    "raise a question about what <PREVIOUS_THINKER> means by a certain term",
    "suggest a different way of thinking about this topic",
    "try to summarize <PREVIOUS_THINKER>'s point in a more elaborate way",
    ]
    prompt_text = """

    <META>

    ***

    Here is part of a script that we are working on, a conversation between some people.

    <PREVIOUS>

    ***
    
    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    This question should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone.
    This question should <RHETGOAL>.
    Do not refer to <THINKER> in the 3rd person.  Remember: you ARE <THINKER>.
    Only write the next dialogue by <THINKER>.  Don't continue the dialogue by imagining what other characters would say in reply.


    <THINKER>: <<PREFIX>""" 
    prompt_text = prompt_text.replace("<META>",meta_dialogue_instruction)
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


  def _consider_art_secret_prompt(self):
    print('art')
    art = self.artworks.pop(0) ## take first
    self.artworks.append(art) ## and put on end
    prefix = "What you are saying, %s, reminds me of this artwork above us, %s. In this" % (self.previous_thinker.name,art)
    prompt_text = """

    <META>

    ***

    Here is part of a script that we are working on, a conversation between some people.

    <PREVIOUS>

    ***

    ***
    Write ONLY the next utterance in the conversation by <THINKER>, <LONGNAME>, in response to the last statement by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    This response should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone.
    This response should also reflect on the topic conversation in light of the famous artwork, <ART>.  It should make clever, specific connections between this artwork and the topic, perhaps interpreting this artwork symbolically.
    Do not refer to <THINKER> in the 3rd person.  Remember: you ARE <THINKER>.
    200-300 words.  Make sure at the end you have punctuation and then the > symbol.

    <THINKER>: <<PREFIX>""" 
    prompt_text = prompt_text.replace("<META>",meta_dialogue_instruction)
    prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
    prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
    prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
    prompt_text = prompt_text.replace("<ART>",art)
    prompt_text = prompt_text.replace("<PREFIX>",prefix)
    return {"prompt":prompt_text,"prefix":prefix}


  def _elaborate_secret_prompt(self,text):
    print('elaborate')
    modes = self.current_thinker.modes
    mode = random.choice(modes)
    nextword = random.choice(["The","A","True,","Let's","Allow me","Perhaps","No,","Although"])
    prefix = " "+nextword
    prompt_text = """

    (Continue the essay below, adding around 300 to 400 words.
    This response should be in the style of <THINKER>, <LONGNAME>.  It should be in the style of <THINKER>'s published writing, using words that <THINKER> often used. It should possess <STYLE>.  Very important: it should <MODE>.
    In other words, it should be a fake essay by <THINKER>.)

    <TEXT> <PREFIX>"""
    prompt_text = prompt_text.replace("<QUESTION>",self.question)
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
    prompt_text = prompt_text.replace("<MODE>",mode)
    prompt_text = prompt_text.replace("<TEXT>",text)
    prompt_text = prompt_text.replace("<PREFIX>",prefix)
    return {"prompt":prompt_text,"prefix":prefix}


  def _general(self,prompt_text):
    print('general')
    prompt_text = prompt_text.replace("<META>",meta_dialogue_instruction)
    prompt_text = prompt_text.replace("<PREVIOUS>",rdp.get_last_bit_of_text(self.current_text))
    prompt_text = prompt_text.replace("<QUESTION>",self.question)
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
    prompt_text = prompt_text.replace("<KEYWORD>",random.choice(self.previous_thinker.words))
    return {"prompt":prompt_text,"prefix":prefix}


  def elaborate(self):
    to_elaborate = rdp.excerpt_last_utterance(self.current_text)
    fake_stub = self._elaborate_secret_prompt(to_elaborate)
    self.current_text = self.current_text.rstrip('>').rstrip(" ") ## remove
    if fake_stub["prefix"]!=None:
      self.current_text+=fake_stub["prefix"]
    elaboration_text = gpt_interface.gpt3_from_prompt(fake_stub['prompt'],max_tokens=600,stop=">")
    #self.current_text += elaboration_text
    rdp.simple_regex_heal(self.current_text) ## always heal after elaboration in case something got messed up

  def _possibly_elaborate(self):
    """
    possibly elaborate once
    """
    if (self.current_thinker.is_player==False and self.reader_question==False): ## don't elaborate when player
      if (random.random()<self.current_thinker.chattiness and self.direct_question_asked==False):
        self.elaborate()

  def _handle_user_question(self):
    self.qa.ingest_text(self.current_text)
    a_question = self.qa.question()
    socrates_question = '\n\nSocrates: <%s, %s>' % (self.current_thinker.name,a_question)
    player_text = input("%s\n>" % socrates_question)
    if len(player_text)!=0: 
      self.current_text+='\n\nSocrates: <%s, %s>' % (self.current_thinker.name,a_question)
      self.current_text+='\n\n%s: <%s>' % (self.current_thinker.name,player_text)
      if player_text.rstrip().endswith("?"):
        self.direct_question_asked =True
    else:
      self.reader_question = True
      self.current_text+='\n\n  **Socrates cranes his neck to look at you.**'
      self.current_text+='\n\n**Socrates: <%s, %s>**' % ("Reader",a_question)
      self.current_text+='\n\n  **...**\n  **...**\n  **...**\n'
      self.current_text+='\n\n  **After an awkward interval Socrates is rebuffed by your silence and turns back around**\n'
      self.current_text+='\n\n  **For your own benefit, take a moment to write down your answer in the lines below:**\n  **______________________________**\n  **______________________________**\n  **______________________________**\n\n'
      self.current_thinker = self.previous_thinker  ## don't remember that current_thinker was player

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
    if self.first_statement_needed==True: ## if socrates has asked a question
      if random.random()<.6:  ## maybe don't immediately switch off this need
        self.first_statement_needed = False ## switch it off
      self.current_text += self._prompt2text(self._refer_to_keyword_secret_prompt())  ## standard response
    elif self.direct_question_asked==True: ## if a question has been asked
      self.direct_question_asked=False ## switch off this need
      self.current_text += self._prompt2text(self._refer_to_keyword_secret_prompt()) ## standard response will do for response to questions
    else:
      if random.random()<self.current_thinker.curiosity: ## QUESTION
        self.direct_question_asked = True # set variable so will know to return to questioned person
        if (random.random()<.3 and self.current_thinker.name=="Socrates"):
          self.current_text += self._ask_fine_tuned_question() 
        else:
          self.current_text+= self._prompt2text(self._ask_question_secret_prompt())
      elif random.random()<.3: # ART (rarely)
        self.current_text+= self._prompt2text(self._consider_art_secret_prompt())
      elif (random.random()<.9 and self.current_thinker.ideas!=None): ## IDEA 
        self.current_text+= self._prompt2text(self._refer_to_quote_or_idea_secret_prompt())
      else: ## how likely to just go with standard prompt
        self.current_text+= self._prompt2text(self._refer_to_keyword_secret_prompt())
    rdp.simple_regex_heal(self.current_text)
    self._possibly_elaborate()


  def _prompt2text(self,prompt):
    stub = '\n\n%s: <' % self.current_thinker.name
    if prompt["prefix"]!=None:
      stub+=prompt["prefix"]
    gpt_text = gpt_interface.gpt3_from_prompt(rdp.decomment_and_snip(self.current_text)+prompt['prompt'],max_tokens=500,stop=">")
    return stub + gpt_text + ">"


  def generate_next_line(self):
    """
    this handles both human and bot turns
    """
    if (self.current_thinker.is_player==True and self.interrupt==True):
      self.current_text+='\n\n%s: <%s>' % (self.current_thinker.name,self.interrupt_text)
      self.interrupt_text=""# reset
    elif self.current_thinker.is_player==True:
      self._handle_user_question()
    else:
      self._generate_next_text()

  def _possibly_psychotrope(self):
    # print(self.current_thinker)
    # print(self.current_thinker.psychotropics)
    for psy in self.current_thinker.psychotropics:
      # print("attempting transform")
      # print(psy)
      last_utterance = rdp.excerpt_last_utterance(self.current_text)
      transformed = psytransform.transform_text(last_utterance,self.current_thinker.psychotropics[psy]['function'],self.current_thinker.psychotropics[psy]['prob'])
      self.current_text = rdp.replace_last_instance(self.current_text,last_utterance,transformed)


  def _possibly_describe(self):
    self.description_adder.possible_action()
    self.current_text+=self.description_adder.flush_text()


  def add_toxicology_report(self):
    self.current_text+=self.description_adder.blood_test_text()


  # def _simple_heal(self):
  #   self.current_text = rdp.simple_regex_heal(self.current_text)


  def next(self):
    print(colored(self.current_text,"red"))
    print(colored((self.previous_thinker.name if self.previous_thinker!=None else None ,self.current_thinker.name),'blue'))
    self._next_thinker()    ## change who is talking
    print(colored((self.previous_thinker.name if self.previous_thinker!=None else None ,self.current_thinker.name),'green'))
    self.reader_question = False  ## has to go after _next_thinker, so maybe should be inside it?
    self.generate_next_line() ## generate the next line
    self._possibly_psychotrope() ## maybe get weird
    self._possibly_describe() ## maybe add description of events
    if self.initial_question_responded == False: ## just keep track of when first person has gone
      self.initial_question_responded = True ## in response to socrates, so he doesn't ask player question immediately
    

  def generate(self,n=10,toxicology_needed=True):
    for i in range(n):
      self.next()
      time.sleep(1)
    if self.direct_question_asked==True: ## don't end with question
      #print("one more turn answer questions")
      self.next()
    if toxicology_needed==True:
      self.add_toxicology_report()

