import gpt_interface


prompt = """

An "odd parenthetical statement" is one that reveals a secret desire, an angry wish, or a neurotic impulse.  It begins "o." It can be vulgar and perverse.  Often it is ungrammatical.

Here is a sentence:

INPUT:"The problem was popularized by René Descartes in the 17th century, resulting in Cartesian dualism, and by pre-Aristotelian philosophers, in Avicennian philosophy, and in earlier Asian traditions." 

Here is an example of adding an "odd parenthetical statement" to this sentence: 

Output:"The problem was popularized by René Descartes in the 17th century, resulting in Cartesian dualism (o i notice that double body go wubba wubba), and by pre-Aristotelian philosophers, in Avicennian philosophy, and in earlier Asian traditions." 

Notice that it is strange, sexual, and informal.

Here is another sentence:

INPUT:"Capital comes initially from circulation, and, moreover, its point of departure is money."

Here is an example of adding an "odd parenthetical statement of yearning" to this sentence: 

OUTPUT:"Capital comes initially from circulation, and, moreover, its point of departure is money (o my yummy num my money mommy money mommy)."

Notice that this expresses some kind of latent Oedipal drive and is embarrassing, not something someone would say except in private.

Here is another sentence:

INPUT:"In the realm of suffering, affliction is something quite apart, specific and irreducible."

OUTPUT:"In the realm of suffering, affliction (o i wish mine enemies would be turned into rancid pink pink pink smoothies) is something quite apart, specific and irreducible."

Notice that this expresses a vulgar anger. 

Take the following sentence and add an "odd parenthetical statement" to it that is perverse and negative, angry perhaps sexual, and very ungrammatical, perhaps with repetition.  It should be creative and new new weird words having to do with technology, food, and the body.

INPUT:"%s"

OUTPUT:"

"""

def add_odd_parenthetical(input_sentence, prompt=prompt):
	prompt = prompt % input_sentence
	return gpt_interface.gpt3_from_prompt(prompt).rstrip('"')

def main():
    prompt = "The captial of France is Paris, a nice place with many people and lots of art."
    print(add_odd_parenthetical(prompt))

if __name__ == '__main__':
    main()

