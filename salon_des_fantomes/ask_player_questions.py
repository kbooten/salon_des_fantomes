
import raw_dialogue_parsing as rdp

with open('data/art.txt','r') as f:
  artworks = [a.rstrip("\n") for a in f.readlines()]

# with open('data/quotes_and_ideas/player.txt','r') as f:
#     player_ideas = [c for c in [i.rstrip("/n") for i in f.readlines()] if len(c)>1]

# with open('data/quotes_and_ideas/player_concepts.txt','r') as f:
#     theoretical_concepts = [c for c in [i.rstrip("/n") for i in f.readlines()] if len(c)>1]


import random

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk import pos_tag,RegexpParser

from nltk.corpus import stopwords
stops = stopwords.words('english')
stops+=["things","thing","stuff","anything"]

class QuestionAsker:

    def __init__(self,player):
        self.player = player
        self.author_utterance_tuples = []
        self.comment_functions = [
            self.COMMENT_on_last_text_random_sentence,
            self.COMMENT_general,
            self.COMMENT_general,
            self.COMMENT_general,
            self.COMMENT_general,
            self.COMMENT_art,
            self.COMMENT_on_small_chunk,
            self.COMMENT_with_player_idea,
        ]

    def ingest_text(self,raw_text):
        self.author_utterance_tuples = rdp.get_author_utterance_tuples(raw_text)


    def COMMENT_art(self):
        #last_author,last_utterance =  self.author_utterance_tuples[-1]
        piece_of_art = random.choice(artworks)
        piece_of_art = piece_of_art.split(",")[0] ## sometimes there is further description after a comma
        return "I wonder if you might draw a connection to this other artwork before us, %s." % (piece_of_art) 


    def COMMENT_on_small_chunk(self):
        last_author,last_utterance =  self.author_utterance_tuples[-1]
        grammar = """
            chunk: {<DT>?<JJ>*<NN.*>}
            chunk: {<JJ>*<NN.*>}
            chunk: {<IN><DT>?<JJ>*<NN.*>}
            chunk: {<NN.*>}
            chunk: {<DT>?<JJ>*<NN.*><DT>?<IN><JJ>*<NN.*>}
        """
        chunks = []
        pos_tagged = pos_tag(word_tokenize(last_utterance))
        parser = RegexpParser(grammar, loop=2)
        parsed = parser.parse(pos_tagged)
        for subtree in parsed.subtrees():
            if subtree.label() == 'chunk': 
                chunks.append(" ".join([token for token,tag in subtree.leaves()]))
        if len(chunks)==0:
            return None
        if random.random()<.7:
            random_chunk = chunks[-1]
        else:
            random_chunk = random.choice(chunks)
        return "Question or critique how we should understand \"%s.\"" % (random_chunk)


    def COMMENT_with_player_idea(self):
        last_author,last_utterance =  self.author_utterance_tuples[-1]
        idea = random.choice(self.player.ideas)
        return "Comment on what %s has said in light of the idea that %s." % (last_author,idea)

    # def COMMENT_with_theory_word(self):
    #     concepts = random.choice(theoretical_concepts)
    #     last_author,last_utterance =  self.author_utterance_tuples[-1]
    #     idea = random.choice(player_ideas)
    #     return "Comment on what %s has said in light of the concept of %s." % (last_author,concept)

    def COMMENT_on_last_text_random_sentence(self):
        last_author,last_utterance =  self.author_utterance_tuples[-1]
        sentences = sent_tokenize(last_utterance)
        #
        provocations = [
            "Why not rephrase this in your own words to make sure you grasp this point.",
            "Provide another piece of evidence.",
            "Reflect on this in light of personal experience.",
            "Reflect on this in light of what you know about history.",
            "Try to cleverly connect this to a bit of high theory that you like to jabber on about.",
            "Continue this thought.",
            "Continue this thought.",
            "Continue this thought.",
            "Make this point in a more interesting way.",
            "Make this point in a more interesting way."
            "Support this.",
            "Critique this."
        ]
        #
        question_provocations = [
            "What do you think?",
            "Answer this in light of personal experience.",
            "Reflect on this question in light of what you know about history.",
        ]
        #
        if len(sentences)==1:
            if sentences[0][-1]=="?": # question
                provocation = random.choice(question_provocations)
            else:
                provocation = random.choice(provocations)
            return "Think about what %s just said. %s" % (last_author,provocation)
        else:
            random_sentence = random.choice(sent_tokenize(last_utterance))
            if random_sentence[-1]=="?": # question
                provocation = random.choice(question_provocations)
            else:
                provocation = random.choice(provocations)
            return "%s has said \"%s\" %s" % (last_author,random_sentence,provocation)

    def COMMENT_general(self):
        provocations = []
        perspectives = ["Marxist","normie lib","nihilist","feminist","accelerationist","ironic","Romantic","good natured","imaginative"] 
        for p in perspectives:
            prov = "Reply from a %s perspective." % p
            prov = prov.replace("a i","an i") ## should use regex
            prov = prov.replace("a a","an e")
            provocations.append(prov)
        return random.choice(provocations)

    def COMMENT_general(self):
        provocations = [
            "Do you agree?",
            "Respond.",
            "Do you agree?",
            "Respond.",
            "Do you agree?",
            "Respond.",
            "Ask a question that brings us back to the question with which I began this conversation.",
        ]
        return random.choice(provocations)


    def question(self):
        c = 0
        comment = None
        while comment == None:
            cf = random.choice(self.comment_functions)
            comment = cf()
            c+=1
            if c>10: ## probably won't trigger but just avoid infinite loop
                break    
        return comment



def main():
    test_text = """

Socrates: "Why is art so boring?"

Freud: "One possible reason art may seem boring to some, is that they are not attuned to the frequency of the libido. The patient may be experiencing a sense of boredom because they are not attuned to the frequency of the libido. This can lead to a feeling of emptiness, or what we call 'the uncanny'. The patient may also feel a sense of dread, as if something is about to happen which will be unpleasant. These strange symptoms are often due to unresolved

Simone Weil: "My question for you, Freud, is this: do you think that art can help us to understand and resolve the feelings of boredom or emptiness associated with the libido?"

Freud: "Art can certainly help us to understand the feelings of boredom or emptiness associated with the libido. It may even help us to resolve them, but only if we are willing to engage in a process of self-examination and confront our own resistances."

Kyle: "I think that art and self-examinatino can be good too."

Freud: "For art to be helpful in resolving the feelings of boredom or emptiness associated with the libido, we must be willing to engage in a process of self-examination and confront our own resistances.

"Simone Weil: "I think that art can help us to understand the feelings of boredom or emptiness associated with the libido. It may even Last night I had a dream that I was in a dark room and there was a shining lightbulb in the middle of the room. Suddenly, someone turned off the light bulb and I was plunged into darkness. In the darkness, I could hear voices whispering my name. The voice sounded like it belonged to my mother. Then she said 'S

Heidegger: "Let's think about the word 'theology' for a moment. What does it mean? It comes from two Greek words: 'theos' meaning God, and 'logos' meaning reason or discourse. So theology is literally the study of God using human reason. Theology is thus the ontic discourse of that which we call 'God'. But what do we mean by 'God'? What is this thing that we are trying to understand when we talk about God? Heidegger went on: "There have been many different conceptions of God throughout history. For some, God is an all- The word 'God' is often used to designate a being that is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history. For The word 'God' is often used to designate a being that is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history. For Many of these conceptions of God are based on the idea of a being who is all-powerful, all-knowing, and all-good. But what do we really mean by this? What are we trying to understand when we talk about such a being?" Heidegger went on: "There have been many different conceptions of God throughout history

Mao: "That's an interesting way of looking at it. I agree that we need to understand what we mean by 'God' before we can talk about theology. But I think there's more to it than just human reason. We also need to have faith."

Socrates: "Could you elaborate on what you mean by 'faith'?"

Mao: "By faith, I mean a belief in something without evidence. It's similar to trust. We need to have faith that the Party is always right, even when we can't see the evidence. It's obvious that you bourgeois intellectuals don't understand faith. You rely on evidence and reason, but that's not enough. We need to have faith in the Party, even when we can't see the evidence. The proletariat cannot be led by individuals who lack faith. It's obvious that you bourgeois intellectuals don't understand faith. You rely on evidence and reason, but that's not enough. We need to have faith in the Party, even when we can't see the evidence. The proletariat cannot be led by individuals who lack faith."Mao went on: "The working class needs a party that they

Freud: "Here, it seems that you are saying two things: first, that the proletariat cannot be led by individuals who lack faith, and second, that we need to have faith in the Party. But what I want to know is this: why do you think that the working class needs a party? And what role does faith play in this?"


  **Frantz Fanon took a sip of port.**


Freud took a sip of sherry.

"""
    import persons
    characters = persons.get_people()
    player = [c for c in characters if c.is_player][0]
    qa = QuestionAsker(player)
    qa.ingest_text(test_text)
    print(qa.question())
    for cf in qa.comment_functions:
        print(cf())


if __name__ == '__main__':
    main()
        


