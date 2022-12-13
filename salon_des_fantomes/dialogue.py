import random,time,re

import gpt_interface

import psytransform

import raw_dialogue_parsing as rdp

with open('data/art.txt','r') as f:
  artworks = [a.rstrip("\n") for a in f.readlines()]


## using signal for timeout on user input
# import signal
# #
# class AlarmException(Exception): # https://stackoverflow.com/q/27013127, https://stackoverflow.com/a/27014090, https://stackoverflow.com/a/494273
#     pass
# #
# def signal_handler(signum, frame):
#   raise AlarmException("user took to long")
#
#signal.signal(signal.SIGALRM, signal_handler)


from ask_player_questions import QuestionAsker
qa = QuestionAsker()

class Dialogue:


  def __init__(self,characters,question,description_adder):
    self.question = question
    self.description_adder = description_adder
    self.temperature=0.9
    self.max_tokens=70
    self.current_text = ""#prompt_prelude
    self.previous_thinker = None
    # self.current_thinker = [t for t in characters if t.name=="Socrates"][0]
    self.direct_question_asked = False
    self.first_statement_needed = True
    #self.suffix = '."'
    self.all_characters = characters
    self._get_start_char()
    self._start_prompt()
    self._create_start_question()
    self.initial_question_responded = False
    self.artworks = artworks.copy()
    random.shuffle(self.artworks)
    self.reader_question = False
    self.player = [c for c in characters if c.is_player][0]


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
    p+="\n\n\n"
    self.current_text+=p


  def _create_start_question(self):
    question = '%s: "%s"' % (self.current_thinker.name,self.question)
    self.current_text += question


  def _next_thinker(self):
    if self.direct_question_asked==True: ## question has been asked, need to return to it
      self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker #swap
    else:
      if self.initial_question_responded == False: 
        ## don't player player at first
        ## because this would cause socrates to follow socrates, since socrates always asks player question 
        thinkers_available = [k for k in self.all_characters if (k!=self.current_thinker and k.is_player==False)]
        thinker = random.choice(thinkers_available)
        self.previous_thinker = self.current_thinker
        self.current_thinker = thinker
      else:
        print("previous_thinker")
        print(self.previous_thinker)
        # if (self.previous_thinker.is_player==True): ## if I've just recently written something
        #   input("should we go again?")
        #   if random.random()<.8:
        #     self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker #swap
        if (self.current_thinker.is_player==False and self.reader_question==False):
          if random.random()<.3:
            self.previous_thinker = self.current_thinker
            self.current_thinker = self.player
        else:
          ## just randomly go to someone else next
          thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
      ## change the thinker, but save previous
          thinker = random.choice(thinkers_available)
          self.previous_thinker = self.current_thinker
          self.current_thinker = thinker


  def _generate_secret_prompt(self):
    """
    the function that actually decides what kind of utterance is next
    """
    if self.first_statement_needed==True: ## if socrates has asked a question
      if random.random()<.4:  ## maybe don't immediately switch off this need
        self.first_statement_needed = False ## switch it off
      return self._refer_to_keyword_secret_prompt()  ## standard response
    elif self.direct_question_asked==True: ## if a question has been asked
      self.direct_question_asked=False ## switch off this need
      return self._refer_to_keyword_secret_prompt() ## standard response will do for response to questions
    else:
      if random.random()<self.current_thinker.curiosity: ## QUESTION
          self.direct_question_asked = True # set variable so will know to return to questioned person
          return self._ask_question_secret_prompt()
      elif random.random()<.3: # ART (rarely)
        return self._consider_art_secret_prompt()
      elif random.random()<.9 and self.current_thinker.ideas!=None: ## IDEA 
        return self._refer_to_quote_or_idea_secret_prompt()
      else: ## how likely to just go with standard prompt
        return self._refer_to_keyword_secret_prompt()


  def _refer_to_keyword_secret_prompt(self):
    print('main')
    if random.random()<.7:
      prefix = random.choice(
        ["So","Hmmm...I suppose that","There may be",
        "On the other","That's","Maybe","Certainly","A","While",
        "My","Your","My dear","Let's","One","A","Here's one way of putting it",
        "To be precise,","At the risk","Now","For","Yet","Let's imagine"]
        )
    else:
      prefix = ""
    ## build prompt
    prompt_text = """

    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by <PREVIOUS_THINKER>.
    This utterance should obey the following rules perfecty:
    1. Important!: It should give detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    2. Important!: It should be in the style of <THINKER>'s published writing, using grammar and syntax that <THINKER> would use.
    3. Important!: It should also possess a VERY <DISPOSITION> tone and should feature <STYLE>.
    4. Important!: It should use three other words that <THINKER> would typically use and that other authors would not.
    5. Important!: It should include the word <KEYWORD> in the first one or two sentences. 
    6. Important!: It should not repeat itself. Each sentence should offer a new idea.
    7. Important!: It should end by closing the quotation mark.

    <THINKER>: "<PREFIX>""" 

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

    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    <THINKER> is <LONGNAME>.
    This response should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone.
    End by closing the quotation mark.

    <THINKER>: "<PREFIX>""" 

    if quote_or_idea.endswith('"'): # quote
      prefix = 'Allow me to connect this question we are discussing to something I once wrote: %s' % quote_or_idea
    else: ## idea
      prefix = "What you are saying reminds me a bit of the fact that %s" % quote_or_idea
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

    Write ONLY what <THINKER>, <LONGNAME>, would say in response to the last statement by by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    This question should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone.
    This question should <RHETGOAL>.
    End by closing the quotation mark.


    <THINKER>: "<PREFIX>""" 
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

    Write ONLY the next utterance in the conversation by <THINKER>, <LONGNAME>, in response to the last statement by <PREVIOUS_THINKER>, giving detailed philosophical reasons and specific rationale for agreeing or disagreeing.
    This response should be in the style of <THINKER>'s published writing. It should possess <STYLE>. It should also possess a <DISPOSITION> tone.
    This response should also reflect on the topic conversation in light of the famous artwork, <ART>.  It should make clever connections between this artwork and the topic, perhaps interpreting this artwork symbolically.
    End by closing the quotation mark.

    <THINKER>: "<PREFIX>""" 
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
    prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
    prompt_text = prompt_text.replace("<DISPOSITION>",random.choice(self.current_thinker.dispositions))
    prompt_text = prompt_text.replace("<ART>",art)
    prompt_text = prompt_text.replace("<PREFIX>",prefix)
    return {"prompt":prompt_text,"prefix":prefix}


  def _elaborate_secret_prompt(self,text):
    print('elaborate')
    modes = ["be coherent, clever, and philosophical"] * 5
    modes += self.current_thinker.modes
    mode = random.choice(modes)
    nextword = random.choice(["The","A","True,","Let's","Allow me","Perhaps","No,","Although"])
    prefix = " "+nextword
    prompt_text = """

    (Continue the essay below, adding around 200 to 300 words.
    This response should be in the style of <THINKER>, <LONGNAME>.  It should be in the style of <THINKER>'s published writing, using words that <THINKER> often used. It should possess <STYLE>.  Very important: it should <MODE>.
    In other words, it should be a fake essay by <THINKER>.)

    <TEXT><PREFIX>"""
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<STYLE>",self.current_thinker.style)
    prompt_text = prompt_text.replace("<MODE>",mode)
    prompt_text = prompt_text.replace("<TEXT>",text)
    prompt_text = prompt_text.replace("<PREFIX>",prefix)
    return {"prompt":prompt_text,"prefix":prefix}


  def _general(self,prompt_text):
    print('general')
    prompt_text = prompt_text.replace("<THINKER>",self.current_thinker.name)
    prompt_text = prompt_text.replace("<LONGNAME>",self.current_thinker.longname)
    prompt_text = prompt_text.replace("<PREVIOUS_THINKER>",self.previous_thinker.name)
    prompt_text = prompt_text.replace("<KEYWORD>",random.choice(self.previous_thinker.words))
    return {"prompt":prompt_text,"prefix":prefix}


  def elaborate(self):
    to_elaborate = rdp.excerpt_last_utterance(self.current_text)
    fake_stub = self._elaborate_secret_prompt(to_elaborate)
    self.current_text = self.current_text.rstrip('"').rstrip(" ") ## remove
    if fake_stub["prefix"]!=None:
      self.current_text+=fake_stub["prefix"]
    elaboration_text = gpt_interface.gpt3_from_prompt(fake_stub['prompt'],max_tokens=600)
    self.current_text += elaboration_text
    self._remove_trailing_whitespace()
    if self.current_text[-1]!='"':
      self.current_text+='"'

  def _possibly_elaborate(self):
    """
    possibly elaborate once
    """
    if (self.current_thinker.is_player==False and self.reader_question==False): ## don't elaborate when player
      if (random.random()<self.current_thinker.chattiness and self.direct_question_asked==False):
        self.elaborate()
    # while True:
    #   if self.current_thinker.is_player==True: ## don't elaborate when player
    #     break
    #   if (random.random()<self.current_thinker.chattiness and self.direct_question_asked==False):
    #     self.elaborate()
    #   else:
    #     break


  def generate_next_line(self):
    if self.current_thinker.is_player==True:
      # print(self.current_text)
      # prepare question using QuestionAsker
      qa.ingest_text(self.current_text)
      a_question = qa.question()
      # set signal to timeout
      #signal.alarm(10) 
      #try:
      socrates_question = '\n\nSocrates: "%s, %s"' % (self.current_thinker.name,a_question)
      player_text = input("%s\n>" % socrates_question)
      #signal.alarm(0) ## reset as soon as possible
      if len(player_text)!=0: 
        self.current_text+='\n\nSocrates: "%s, %s"' % (self.current_thinker.name,a_question)
        self.current_text+='\n\n%s: "%s"' % (self.current_thinker.name,player_text)
        if player_text.rstrip().endswith("?"):
          self.direct_question_asked =True
      #except:
        #signal.alarm(0) ## reset as soon as possible
      else:
        self.reader_question = True
        self.current_text+='\n\n  **Socrates cranes his neck to look at you.**'
        self.current_text+='\n\nSocrates: "%s, %s"' % ("Reader",a_question)
        self.current_text+='\n\n  **...**\n  **...**\n  **...**\n'
        self.current_text+='\n\n  **After an awkward interval Socrates is rebuffed by your silence and turns back around**\n\n'
        self.current_text+='\n\n  **For your own benefit, take a moment to write down your answer in the lines below:**'#\n  **______________________________**\n  **______________________________**\n  **______________________________**\n\n'
        ## don't remember that current_thinker was player
        self.current_thinker = self.previous_thinker  ## this is dubious because but works I think bc next_thinker run soon

    else:
      #fake_stub = prompt_prelude + self._generate_secret_prompt()
      fake_stub = self._generate_secret_prompt()
      #print(fake_stub)
      real_stub = '\n\n%s: "' % self.current_thinker.name
      if fake_stub["prefix"]!=None:
        real_stub+=fake_stub["prefix"]
      self.current_text+=real_stub+gpt_interface.gpt3_from_prompt(rdp.decomment_and_snip(self.current_text)+fake_stub['prompt'])
      self._remove_trailing_whitespace() ## clean up
      ### OPTIONAL
      self._possibly_elaborate() ## <-- elaborate, speaker speaks more
      self._simple_heal() ## <-- deal with any sentences that cut off without trailing punctuation


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


  def _remove_trailing_whitespace(self):
    self.current_text = rdp.remove_trailing_whitespace(self.current_text)


  def _simple_heal(self):
    self.current_text = rdp.simple_regex_heal(self.current_text)


  def next(self):
    self._next_thinker()    ## change who is talking
    self.reader_question = False  ## has to go after _next_thinker, so maybe should be inside it?
    self.generate_next_line() ## generate the next line
    self._possibly_psychotrope() ## maybe get weird
    self._possibly_describe() ## maybe add description of events
    if self.initial_question_responded == False: ## just keep track of when first person has gone
      self.initial_question_responded = True ## in response to socrates, so he doesn't ask player question immediately
    

  def generate(self,n=3,toxicology_needed=True):
    for i in range(n):
      self.next()
      time.sleep(1)
    if self.direct_question_asked==True: ## don't end with question
      #print("one more turn answer questions")
      self.next()
    if toxicology_needed==True:
      self.add_toxicology_report()

