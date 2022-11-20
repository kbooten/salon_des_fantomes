import re

def excerpt_last_utterance_and_transform(raw_dialogue_text):
    utterances = re.findall(r'(?:\: \")(.+)(?:\"$)',raw_dialogue_text,flags=re.M)
    return utterances[-1]


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


def main():
  test_text = """

Socrates: "Why is art so boring?"

Freud: "One possible reason art may seem boring to some, is that they are not attuned to the frequency of the libido. The patient may be experiencing a sense of boredom because they are not attuned to the frequency of the libido. This can lead to a feeling of emptiness, or what we call 'the uncanny'. The patient may also feel a sense of dread, as if something is about to happen which will be unpleasant. These strange symptoms are often due to unresolved

Simone Weil: "My question for you, Freud, is this: do you think that art can help us to understand and resolve the feelings of boredom or emptiness associated with the libido?"

Freud: "Art can certainly help us to understand the feelings of boredom or emptiness associated with the libido. It may even help us to resolve them, but only if we are willing to engage in a process of self-examination and confront our own resistances."

Kyle: "I think that art and self-examinatino can be good too."

Freud: "For art to be helpful in resolving the feelings of boredom or emptiness associated with the libido, we must be willing to engage in a process of self-examination and confront our own resistances."Simone Weil: "I think that art can help us to understand the feelings of boredom or emptiness associated with the libido. It may even Last night I had a dream that I was in a dark room and there was a shining lightbulb in the middle of the room. Suddenly, someone turned off the light bulb and I was plunged into darkness. In the darkness, I could hear voices whispering my name. The voice sounded like it belonged to my mother. Then she said 'S

Heidegger: "Let's think about the word 'theology' for a moment. What does it mean? It comes from two Greek words: 'theos' meaning God, and 'logos' meaning reason or discourse. So theology is literally the study of God using human reason. Theology is thus the ontic discourse of that which we call 'God'. But what do we mean by 'God'? What is this thing that we are trying to understand when we talk about God? Heidegger went on: "There have been many different conceptions of God throughout history. For some, God is an all- The word 'God' is often used to designate a being that is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history. For The word 'God' is often used to designate a being that is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history. For Many of these conceptions of God are based on the idea of a being who is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history

Mao: "That's an interesting way of looking at it. I agree that we need to understand what we mean by 'God' before we can talk about theology. But I think there's more to it than just human reason. We also need to have faith."

Socrates: "Could you elaborate on what you mean by 'faith'?"

Mao: "By faith, I mean a belief in something without evidence. It's similar to trust. We need to have faith that the Party is always right, even when we can't see the evidence. It's obvious that you bourgeois intellectuals don't understand faith. You rely on evidence and reason, but that's not enough. We need to have faith in the Party, even when we can't see the evidence. The proletariat cannot be led by individuals who lack faith. It's obvious that you bourgeois intellectuals don't understand faith. You rely on evidence and reason, but that's not enough. We need to have faith in the Party, even when we can't see the evidence. The proletariat cannot be led by individuals who lack faith."Mao went on: "The working class needs a party that they

Freud: "Here, it seems that you are saying two things: first, that the proletariat cannot be led by individuals who lack faith, and second, that we need to have faith in the Party. But what I want to know is this: why do you think that the working class needs a party? And what role does faith play in this?"


  **Frantz Fanon took a sip of port.**


Freud took a sip of sherry.
  """
  print(test_text)
  print("excerpting last utterance:")
  last_utterance = excerpt_last_utterance_and_transform(test_text)
  print(last_utterance)
  print("testing replacing last utterance:")
  print(replace_last_instance(test_text,last_utterance,"TEST TEST TEST"))
  print("testing remove comments")
  print(remove_comments(test_text))

if __name__ == '__main__':
  main()