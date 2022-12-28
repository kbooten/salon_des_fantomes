import random


###

def _light_lucience():
	phrases = [
		"a birthright thousandfold candle",
		"a torch made of reverse prisms pristine",
		"light within the locket of light",
		"coterminous with truth's energy: light!",
		"all my eyes reflecting that word",
		"the light's hard mercy",
		]
	chosen = random.choice(phrases)
	return chosen

def light_lucience(character):
	character.words.append(_light_lucience())


###

def _juan_crystalsmith():
	phrases = [
		"Juan Crystasmith's miraculous %s",
		]
	chosen = random.choice(phrases)
	return chosen

###

def _new_ideology():
	prefixes = ["anarcho","feminist","communo","post","Latvian","third"]
	cores = ["frog","star","Ikea"]
	characteristics = ["floral",""]
	pre1,pre2 = random.sample(prefixes,2)
	if random.random()<.3:
		pre2=""
	core = random.choice(cores)
	ideology = "%s-%s-%sism" % (pre1,pre2,core)
	ideology.replace("--","-")
	if random.random()<.3:
		characteristic = random.choice(characteristics)
		ideology = ideology+" with %s characteristics" % characteristic
	return "I am more and more sympathetic to the tenets of %s" % ideology

##


def _new_concept():
	prefixes = ["psychonalytic","marxist-materialist","phenomenological","theological","string theoretic"]
	prefixes += ["philosophical"] * 5
	adjs = ["double","forceful","retreating","coterminous","fungible","frangible"]
	nouns = ["concurrence","mold","thought"]
	connections = [" of "," without "," but not "," through "," beyond ","-","/"] ## watch spaces
	if random.random()<.6:
		return "the %s concept of '%s %s'" % (random.choice(prefixes),random.choice(adjs),random.choice(nouns))
	else:
		n1,n2 = random.sample(nouns,2)
		return "the %s concept of '%s%s%s'" % (random.choice(prefixes),n1,random.choice(connections),n2)

def main():
	print(_new_ideology())
	print(_new_concept())

if __name__ == '__main__':
	main()