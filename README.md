# Salon des Fantômes

This is the repo for the code that I used to write *Salon des Fantômes: Or, Streptohormetic Prompt Engineering for the Production of a Jagged Noetic Substrate* (Inside the Castle 2024).  This book documents a philosophical/artistic salon at which I was the only non-AI attendee.   

I completed the code for this project mostly in the fall of 2022, with a bit of tinkering during a five-day residency via Inside the Castle (during which time I was charged with writing a book of exactly one hundred thousand words). 

My code is essentially a very complex and even arcane wrapper for GPT-3.5 (the OpenAI model that was available at the time).  This wrapper contains and does a variety of things.  

## What the code contains:

* a set of "characters" (e.g., a monosyllabic mountain, a Latvian architect), with various dispositions, favorite words and phrases, and interests
* a set of topics of conversations
* a set of paintings and artworks that characters may stumble/remark upon
* a set of psychotropic spells that transform the character or the character's speech in some way

## What the code does:

* instantiates and manages the conversation by, for instance:
	- picking a topic of conversation and a subset of characters to discuss it with me, the human
	- cobbling together prompts that contain limited conversational context (the past `n` words) as well as "secret" information (information that did not end up in the book's text, such as the character's attributes that would define its utterances)
	- parsing the response from the LLM and including it into the text
	- allowing me, the human, to interrupt and speak when I so choose 
	- generating via simple aleatoric means basic contextual information (e.g., about when a character has had a sip of their drink or scratched themselves)
	- keep track of the state of the character's blood and how many parts-per-million of various psychotropic substances it contains (see below)

## Weird Stuff

### Random Word Trick

To combat the tendency of LLMs to be extremely boring, I employed what I call the "random word trick."  At each utterance, the character whose turn it was to speak was instructed to respond using a randomly selected word from one of a hand-composed list of favorite words.  

### Psychotropic Drinks

As they converse, characters sip from drinks.  Some of these drinks---mostly rare and costly vintages of French wine---contain psychotropic potions or spells.  These are functions that either 1) change the data assocated with each character (e.g., adding oddities to this character's favorite words), and thus what they are likely to say, or 2) (more often) directly change a character's utterance, sending it back into the LLM for a round of "post-processing" according to some additional prompt (e.g., to include religious mania).

