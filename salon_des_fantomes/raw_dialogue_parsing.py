import re

def excerpt_last_utterance(raw_dialogue_text):
    """
    gets the last thing someone said, which must be surrounded by quotes
    """
    utterances = re.findall(r'(?:\: \<)(.+)(?:\>$)',raw_dialogue_text,flags=re.M)
    return utterances[-1]

def simple_regex_heal(raw_dialogue_text):
  """
  delete end of utterance if it doesn't have terminal punctuation where it should be (for complete sentence)
  or, if there is no terminal punctuaion at all, just turn into an ellipsis
  """
  if re.search(r'[.?!]',raw_dialogue_text)!=None: ## if has terminal punctuation somewhere
    ## "text1. text2\"" > "text 1.\""
    return re.sub(r'(?<=[.?!])[^.?!]+ {0,}\>? {0,}$','>',raw_dialogue_text,count=1)
  else: 
    ## "text 1" > "text 1...\""
    return re.sub(r' {0,}\>? {0,}?$','...>',raw_dialogue_text,count=1) ## ellipsis, possi

def replace_last_instance(raw_dialogue_text,to_replace,replacement):
  """
  https://stackoverflow.com/a/59082116
  """
  return replacement.join(raw_dialogue_text.rsplit(to_replace, 1)) 

def remove_comments(raw_dialogue_text,despace=True):
  text = re.sub(r'  \*\*.+$',"",raw_dialogue_text,flags=re.M)
  if despace==True: ## remove consecutive newline
    text = re.sub(r'\n{3,}',"\n\n",text)
  return text

def get_author_utterance_tuples(raw_dialogue_text):
  """
  like ("Socrates","whatever socrates says")
  """
  utterances = re.findall(r'^((?:[A-Z][^\s]+)(?:(?: [A-Za-z][^\s]+)){0,})(?:\: \<)(.+)(?:\>$)',raw_dialogue_text,flags=re.M)
  return utterances

def get_last_bit_of_text(raw_dialogue_text,n=3):
  """
  returns the last n turns of dialogue
  does this by using a regex to get the indices of "Socrates:" and "Mao:" etc. 
  """
  start_indices_of_utterances = [m.start(0) for m in re.finditer(r'^(?:[A-Z][^\s]+)(?:(?: [A-Za-z][^\s]+)){0,}:',raw_dialogue_text,flags=re.M)] 
  #print(start_indices_of_utterances)
  last_n = start_indices_of_utterances[-n:]
  n_from_last = last_n[0]
  return raw_dialogue_text[n_from_last:] 

def remove_trailing_whitespace(raw_dialogue_text):
  """
  clean up trailing white space which can get added sometimes by gpt
  """
  return re.sub(r'\s+$','',raw_dialogue_text)

def decomment_and_snip(raw_dialogue_text,n=2,clean_up=True):
  """
  just a combination of get_last_bit_of_text and remove_comments
  """
  decommented = remove_comments(raw_dialogue_text)
  decommented_and_snipped = get_last_bit_of_text(decommented,n=n)
  if clean_up==True:
    decommented_and_snipped = decommented_and_snipped.rstrip("\n ")
  return decommented_and_snipped



def main():
  test_text = """

Socrates: <Why is art so boring?>

Freud: <One possible reason art may seem boring to some, is that they are not attuned to the frequency of the libido. The patient may be experiencing a sense of boredom because they are not attuned to the frequency of the libido. This can lead to a feeling of emptiness, or what we call 'the uncanny'. The patient may also feel a sense of dread, as if something is about to happen which will be unpleasant. These strange symptoms are often due to unresolved>

Simone Weil: <My question for you, Freud, is this: do you think that art can help us to understand and resolve the feelings of boredom or emptiness associated with the libido?>

Freud: <Art can certainly help us to understand the feelings of boredom or emptiness associated with the libido. It may even help us to resolve them, but only if we are willing to engage in a process of self-examination and confront our own resistances.>

  **Frantz Fanon took a sip of port.**


  **Freud took a sip of sherry.**

K'yle Ko: <I think that art and self-examinatino can be good too.>


"""
  #print(test_text)
  print(">>excerpting last utterance:")
  last_utterance = excerpt_last_utterance(test_text)
  print(last_utterance)
  # print(">>excepting last utterance and speaker, minus trailing punctuation:")
  # print(text_to_elaborate(test_text))
  print(">>testing replacing last utterance:")
  print(replace_last_instance(test_text,last_utterance,"TEST TEST TEST"))
  print(">>testing remove comments")
  print(remove_comments(test_text))
  print(">>testing getting author utterance tuples")
  print(get_author_utterance_tuples(test_text))
  print('>>testing sampling text')
  print(get_last_bit_of_text(test_text))
  print('>>testing decomment_and_snip')
  print(decomment_and_snip(test_text))
  # print(">>testing broken utterance catcher")
  # print(simple_regex_heal(test_text2))

if __name__ == '__main__':
  main()