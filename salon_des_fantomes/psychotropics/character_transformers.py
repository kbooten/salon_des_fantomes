import random


############# 
# ADD WORDS #
#############

def word_dasani():
	phrases = [
		"a birthright thousandfold Dasani",
		"Dasani, a temperate torch made of reverse prisms pristine",
		"locket of light: Dasani!",
		"coterminous with truth's essences: Dasani!",
		"need a Dasani",
		"crave a Dasani",
		"cool Dasani",
		"just a sip of Dasani",
		"jealous of thy Dasani",
		"unquenchable wetness of Dasani",
		"Dasani is 100%",
		"did you know that Dasani",
		"Dasani's blend of dissolved treasure such as",
		"Dasani's blend of dissolved contradictions such as",
		"Dasani's blend of dissolved empires such as",
		"Dasani's blend of dissolved rocks such as",
		"Dasani's BPA-free",
		"Dasani from the choicest municipal",
		"osmosis of Dasani",
		"Dasani's Recycled PET (rPET)"
		"I love Dasani",
		"I choose always Dasani",
		]
	phrases += ["Dasani"]*10
	chosen = random.choice(phrases)
	return chosen

###

def word_on_indolence():
	lines = [
		"one behind the other stepp'd serene in placid sandals",
		"they pass'd, like figures on a marble urn",
		"How is it, Shadows! that I knew ye not?",
		"How came ye muffled in so hush a mask?",
		"leave my sense unhaunted quite of all but — nothingness?",
		"They faded, and, forsooth! I wanted wings",
		"O Shadows!",
		"Ghosts, adieu! Ye cannot raise my head cool-bedded",
		"Farewell! I yet have visions for the night",
		"Vanish, ye Phantoms! from my idle spright",
	]
	return random.choice(lines)


###

def word_juan():
	phrases = [
		"Juan Crystalsmith's miraculous face",
		]
	chosen = random.choice(phrases)
	return chosen

###

def word_new_ideology():
	prefixes = ["anarcho","feminist","communo","post","third","new","anti","poly"]
	cores = ["species","Ikea","forest","number","communal","minimal","maximal","mon","emotion","syncret","phylet"]
	characteristics = ["floral","Latvian","Slavic","Levantine"]
	pre1,pre2 = random.sample(prefixes,2)
	if random.random()<.3:
		pre2=""
	core = random.choice(cores)
	ideology = "%s-%s-%sism" % (pre1,pre2,core)
	ideology = ideology.replace("--","-")
	if random.random()<.3:
		characteristic = random.choice(characteristics)
		ideology = ideology+" with %s characteristics" % characteristic
	return "I am more and more sympathetic to the tenets of %s" % ideology

##

def word_new_concept():
	prefixes = ["psychonalytic","marxist-materialist","phenomenological","theological","string theoretic"]
	prefixes += ["philosophical"] * 5
	adjs = ["double","simple","chaotic","forceful","retreating","coterminous","fungible","frangible","mercy","reverse","universal","sudden"]
	nouns = ["concurrence","mold","thought","purchase","signal","point","identity","haecceity","costume","force","Ananke","proof","wire","quantity","number","slime"]
	connections = [" of "," without "," but not "," through "," beyond ","-","/"] ## watch spaces
	if random.random()<.6:
		return "the %s concept of '%s %s'" % (random.choice(prefixes),random.choice(adjs),random.choice(nouns))
	else:
		n1,n2 = random.sample(nouns,2)
		return "the %s concept of '%s%s%s'" % (random.choice(prefixes),n1,random.choice(connections),n2)


## 

def word_meta_gesture():
	titles = ["Salon Des Fantômes"] * 9
	titles+= ["Hell's Lavatory"]
	things = ["field","book","poem","discourse prison","gymnasion","discourse event","thought-generating torture device","10^21-year Naraka","literary event","virtual cabinet","parlor game","conversation","teacherless school","piece of educational software","Naraka","double stimulation","double simulation"]
	sentences = [
		"I feel like I'm in a %s called %s",
		"I'm beginning to suspect that we are in a %s called %s",
		"I'm beginning to suspect that we are in a %s called %s",
		"What if this is all a %s called %s?",
		"What if this is all a %s called %s?",
		"Let's assume that, because of our sins, we are in a %s called %s",
		"Let's assume that, as a reward for lives spent wisely in wise discourse, we are in a %s called %s",
	]
	return random.choice(sentences)%(random.choice(things),random.choice(titles))


####

def mode_juan():
	modes = [
		"Draw a connection to the mythical life of Juan Crystalsmith, an enigmatic savior who could put one's grief inside a cactus, an owl, or something like that.",
		"Draw a connection to the sermon of Juan Crystalsmith to the empty desert, quoting enigmatic fables that he may have told to guide us on the path between entropy and negentropy, or to help us become properly intersymbiotic.",
		"Draw a connection to the ways that Juan Crystalsmith was persecuted by criminals and lawmen, by pirates and tax-collectors, by the old and the young, the stern and the soft---persecuted for his hard mercy and his enigmas.",
	]
	return random.choice(modes)


def mode_self_abnegation():
	modes = [
		"Express serious doubt about one's own ideas.",
		"Confess to a mental or spiritual limitation that one possesses.",
	]
	return random.choice(modes)

def disposition_sorrow():
	return "sorrowful"


def main():
	print(word_dasani())
	print(word_juan())
	print(word_new_ideology())
	print(word_new_concept())
	print(word_meta_gesture())
	print(word_on_indolence())
	print(mode_juan())
	print(mode_self_abnegation())



if __name__ == '__main__':
	main()