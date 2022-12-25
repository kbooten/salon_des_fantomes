import random

def tf0():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

def tf1():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

def tf2():
	adjs = range(2,400)
	nouns = ["thoughts","voices","urges"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%d %s" % (a,n)

def tf3():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

def tf4():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

def tf5():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

def tf6():
	adjs = ["wool","mud","silt","green"]
	nouns = ["yogurt","woman","moss"]
	a = random.choice(adjs)
	n = random.choice(nouns)
	return "%s %s" % (a,n)

# def tf3():
# 	glyphs = ["a",""]
# 	nouns = ["thoughts","voices","urges"]
# 	a = random.choice(adjs)
# 	n = random.choice(nouns)
# 	return "%d %s" % (a,n)


def main():
	print(tf1())
	print(tf2())

if __name__ == '__main__':
	main()