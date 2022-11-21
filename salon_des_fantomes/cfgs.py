from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

my_grammar1 = """

S -> S1
S1 -> "like" NP
NP -> NN | DT NN | DT JJ NN | DT JJ IN DT NN
DT -> "the" | "a" | "your"
NN -> "rabbit" | "breath" | "leather" 
JJ -> "interluded"

"""

my_grammar2 = """

S -> S1
S1 -> UH | UH HM | UH HM WOW | UH HMM WOW UM | UH HMM WOW UM SHIT
UH -> "uh" | "whuh" | "huhh"
HM -> "hmm" | "hmmmmm" | "hmmmmmmMM" | "hmmmmmmMMMMM!" | "HMMMMMM!"
WOW -> "is that" | "uh like" 
SHIT -> "damn" | "nice" | "damn right" 

"""

# cfg1 = {"generator":CFG.fromstring(my_grammar1),"joiner":" "}
# cfg2 = {"generator":CFG.fromstring(my_grammar2),"joiner":"..."}

class CFGDescription:

	def __init__(self,grammar,joiner=" ",fallback="matter"):
		self.generator = generate(CFG.fromstring(grammar))
		self.fallback = fallback
		self.joiner = joiner

	def my_next(self):
		try:
			return self.joiner.join(next(self.generator))
		except StopIteration:
			return self.fallback

cfg1 = CFGDescription(my_grammar1)
cfg2 = CFGDescription(my_grammar2,joiner="...")
