import random,time,re

import gpt_interface

import psytransform

import raw_dialogue_parsing as rdp


class Dialogue:

  def __init__(self,characters,question,description_adder):
    self.question = question
    self.description_adder = description_adder
    self.temperature=0.9
    self.max_tokens=70
    self.current_text = ""#prompt_prelude
    self.previous_thinker = None
    # self.current_thinker = [t for t in characters if t.name=="Socrates"][0]
    self.current_discourse_move = "ask a question"
    self.person_to_discourse_moves = {}
    self.direct_question_asked = False
    self.first_statement_needed = True
    #self.suffix = '."'
    self.all_characters = characters
    self._get_start_char()
    self._start_prompt()
    self._create_start_question()

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
    p = "The philosophical salon continues.\n\nA group---%s---has gathered in one corner of the room, lounging on sofas." % chars_string
    p+="\n\n\n"
    self.current_text+=p


  def _create_start_question(self):
    question = '%s said: "%s"' % (self.current_thinker.name,self.question)
    self.current_text = question


  def _next_thinker(self):
    if self.direct_question_asked==True: ## question has been asked, need to return to it
      print(self.current_thinker,self.previous_thinker)
      self.current_thinker,self.previous_thinker = self.previous_thinker,self.current_thinker #swap
      print(self.current_thinker,self.previous_thinker)
    else:
      thinkers_available = [k for k in self.all_characters if k!=self.current_thinker]
      thinker = random.choice(thinkers_available)
      self.previous_thinker = self.current_thinker
      self.current_thinker = thinker


  def _generate_secret_prompt(self):
    if self.first_statement_needed==True: ## if socrates has asked a question
      if random.random()<.4:  ## maybe don't immediately switch off this need
        self.first_statement_needed = False ## switch it off
      return self._standard_secret_prompt()  ## standard response
    elif self.direct_question_asked==True: ## if a question has been asked
      self.direct_question_asked=False ## switch off this need
      return self._standard_secret_prompt() ## standard response will do for response to questions
    else:
      if random.random()<self.current_thinker.curiosity:
          self.direct_question_asked = True # set variable so will know to return to questioned person
          return self._question_secret_prompt()
      elif random.random()<.1: # rarely talk about art
        return self._art_secret_prompt()
      else: ## how likely to just go with standard prompt
        return self._standard_secret_prompt()


  def _standard_secret_prompt(self):
    print('main')
    thinker = self.current_thinker.name
    thinker_stub = random.choice(self.current_thinker.words)
    previous_thinker = self.previous_thinker.name
    if random.random()<.7:
      prefix = random.choice(["So","Hmmm...I suppose that","There may be","On the other","That's","Maybe","Certainly","A","While",
                              "My","Your","My dear","Let's","One","A","Here's one way of putting it","To be precise,","At the risk","Now","For"])
    else:
      prefix = ""
    return {"prompt":'\n\nWrite the next utterance the conversation by %s\ \
    in %s\'s style, \
    responding to the immediately previous statement by %s, giving detailed philosophical reasons and specific rationale, agreeing or disagreeing. This next line of dialogue should be 15 to 50 words long, \
    refer to a word or phrase from the previous statement by %s \
    and include the word "%s". End by closing the quotation mark. \
    \n\n%s said: "%s' % (thinker,thinker,previous_thinker,previous_thinker,thinker_stub,thinker,prefix),
    "prefix":prefix}


  def _question_secret_prompt(self):
    print('question')
    thinker = self.current_thinker.name
    thinker_stub = random.choice(self.current_thinker.words)
    previous_thinker = self.previous_thinker.name
    prefix = random.choice(["My","That","Of","What","Clearly","Here","Let","Please","Could you elaborate"])
    return {"prompt":'\n\nWrite the next utterance the conversation by %s, \
    asking %s \
    a throughtful philosophical question about %s\'s immedately previous utterance. This next utterance should be a question of 20 to 50 or so words long.\
    \n\n%s said: "\
    %s' % (thinker,previous_thinker,previous_thinker,thinker,prefix),
    "prefix":prefix}


  def _art_secret_prompt(self):
    print('art')
    thinker = self.current_thinker.name
    thinker_stub = random.choice(self.current_thinker.words)
    previous_thinker = self.previous_thinker.name
    artwork = random.choice([
        "Las Meninas by Velásquez",
        "Dürer's woodcut The Four Horsemen of the Apocalypse",
        "Berthe Morisot's painting of a Woman at Her Toilette",
        "Paul Klee's Twittering Machine",

    ])
    return {"prompt":'\n\nWrite the next utterance the conversation by %s, \
    describing %s \
    and connecting it to the previous statement by %s and giving careful philosophical reasons and specific rationale. End by closing the quotation mark. \
    Be sure to refer to a specific word or idea from %s\'s previous line of dialogue. 50 to 100 words. \
    \n\n%s said: \
    "What you are saying, %s, \
    reminds me of this artwork above us, %s. In this' % (thinker,artwork,previous_thinker,previous_thinker,thinker,previous_thinker,artwork),
    "prefix":"What you are saying, %s, reminds me of this artwork above us, %s.  In this" % (previous_thinker,artwork)}


  def _continue_secret_prompt(self):
    print('elaborate')
    thinker = self.current_thinker.name
    thinker_stub = random.choice(self.current_thinker.words)
    modes = ["be coherent, clever, and philosophical"] * 5
    modes = self.current_thinker.modes + ["make an argument",
      "add some nuance",
      "admit where the other speakers could be correct or are making a good point",
      "define terms carefully",
      "give an anecdote",
      "try to see the other side of the argument",
      "synthesize multiple points made by other people previously in the conversation"]
    mode = random.choice(modes)
    return {"prompt":'\n\nContinue the line above by %s\
    in %s\'s style. This monologue should be 5 to 10 sentences and\
    it should %s.\
    It should use new words, not simply repeat what has been said before.\
    It should also use the word "%s".\
    \n\n%s continued: "' % (thinker,thinker,mode,thinker_stub,thinker),
    "prefix":None}


  def elaborate(self):
    fake_stub = self._continue_secret_prompt()
    self.current_text = self.current_text.rstrip('"') ## prep to add more
    self.current_text+=" "
    #self.current_text+=" ~ "
    self.current_text+=gpt_interface.gpt3_from_prompt(rdp.remove_comments(self.current_text)+fake_stub['prompt'])


  def _possibly_elaborate(self):
    while True:
      if self.current_thinker.is_player==True: ## don't elaborate when player
        break
      if (random.random()<self.current_thinker.chattiness and self.direct_question_asked==False):
        self.elaborate()
      else:
        break


  def generate_next_line(self):
    self._next_thinker()
    if self.current_thinker.is_player==True:
      print(self.current_text)
      player_text = input(">")
      self.current_text+='\n\n%s: "%s"' % (self.current_thinker.name,player_text)
    else:
      #fake_stub = prompt_prelude + self._generate_secret_prompt()
      fake_stub = self._generate_secret_prompt()
      real_stub = '\n\n%s said: "' % self.current_thinker.name
      if fake_stub["prefix"]!=None:
        real_stub+=fake_stub["prefix"]
      self.current_text+=real_stub+gpt_interface.gpt3_from_prompt(rdp.remove_comments(self.current_text)+fake_stub['prompt'])


  def _possibly_psychotrope(self):
    print(self.current_thinker)
    print(self.current_thinker.psychotropics)
    for psy in self.current_thinker.psychotropics:
      print("attempting transform")
      print(psy)
      last_utterance = rdp.excerpt_last_utterance_and_transform(self.current_text)
      transformed = psytransform.transform_text(last_utterance,self.current_thinker.psychotropics[psy]['function'],self.current_thinker.psychotropics[psy]['prob'])
      self.current_text = rdp.replace_last_instance(self.current_text,last_utterance,transformed)


  def _possibly_describe(self):
    self.description_adder.possible_action()
    self.current_text+=self.description_adder.flush_text()

  def add_toxicology_report(self):
    self.current_text+=self.description_adder.blood_test_text()


  def next(self):
    self.generate_next_line()
    self._possibly_elaborate()
    self._clean()
    self._possibly_psychotrope()
    self._possibly_describe()


  def _clean(self):
    self.current_text = re.sub(r" said: ",": ",self.current_text)


  def generate(self,n=6,toxicology_needed=True):
    for i in range(n):
      self.next()
      time.sleep(1)
    if toxicology_needed==True:
      self.add_toxicology_report()
