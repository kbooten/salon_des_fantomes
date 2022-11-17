import gpt_interface


prompt = """

"Adding doubt" is when you take a statement and make it full of expressions of doubt.  

Here is a sentence:

INPUT:"The problem was popularized by René Descartes in the 17th century, resulting in Cartesian dualism, and by pre-Aristotelian philosophers, in Avicennian philosophy, and in earlier Asian traditions." 

Here is an example of "adding doubt" to it:

Output:"The problem may have been popularized by René or was it Ronald Descartes in the 17th century, resulting in Cartesian dualism, I think, maybe, and by pre-Aristotelian philosophers, in Avicennian philosophy though I'm not sure what that is, and in earlier Asian traditions but how much earlier I couldn't say." 

Here is another sentence:

INPUT:"Capital comes initially from circulation, and, moreover, its point of departure is money."

Here is an example of "adding doubt" to it:

OUTPUT:"I think maybe capital comes from circulation...but what if it comes from storage capacity?  Or from labor?  I could have it all wrong."

Here is another sentence:

INPUT:"I have always believed that the realm of suffering, affliction is something quite apart, specific and irreducible.  But maybe we are all always afflicted all the time, and I'm not special atall."

Here is an example of "adding doubt" to it:

OUTPUT:"In the realm of suffering, affliction (o i wish mine enemies would be turned into rancid pink pink pink smoothies) is something quite apart, specific and irreducible."

Take the following sentence and "add doubt" to it.

INPUT:"%s"

OUTPUT:"

"""

def add_doubt(input_sentence, prompt=prompt):
	prompt = prompt % input_sentence
	return gpt_interface.gpt3_from_prompt(prompt).rstrip('"')

def main():
    prompt = "The captial of France is Paris, a nice place with many people and lots of art."
    print(add_doubt(prompt))

if __name__ == '__main__':
    main()

