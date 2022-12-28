import gpt_interface


# instruction = """
# """
prompt = """Take the input and add an "odd parenthetical statement" to it that hints at a strange libidinal desire or wish, that one would be afraid to express in public. It should be creative and contain weird words having to do with organs, machines, relationships, fragrances, and bodily desires.  It should connect in some way to the text it comes after.  It could contain lots of rhyme and alliteration. An odd parenthetical statement is surrounded by parentheses.  It should just express the perverse desire, not actually use words like "desire" or "perverse."

Important: if it already has one or more "odd parenthetical statements," add anothers recursively (one inside the other). 

An "odd parenthetical statement" is one that reveals a secret desire, an angry wish, or a neurotic impulse.  It begins "(o." It can be vulgar and perverse.  Often it is ungrammatical.

Here is an example of adding an "odd parenthetical statement" to some input text: 

INPUT: <The problem was popularized by René Descartes in the 17th century, resulting in Cartesian dualism, and by pre-Aristotelian philosophers, in Avicennian philosophy, and in earlier Asian traditions.>
OUTPUT: <The problem was popularized by René Descartes in the 17th century, resulting in Cartesian dualism (o i notice that double body go wubba wubba my o my), and by pre-Aristotelian philosophers, in Avicennian philosophy, and in earlier Asian traditions.>

Here is another example that involves adding yearning, a latent Oedipal drive and is embarrassing, not something someone would say except in private.

INPUT: <Capital comes initially from circulation, and, moreover, its point of departure is money.>
OUTPUT: <Capital comes initially from circulation, and, moreover, its point of departure is money (o my yummy num my money mommy money mommy).>

Another example:

INPUT: <Capital comes initially from circulation, and, moreover, its point of departure is money.>
OUTPUT: <Capital comes initially from circulation (of my green blood, mmmm mm funk like chypre smoothe) and, moreover, its point of departure is money.>

Here is another example, this one expressing vulgar anger:

INPUT: <In the realm of suffering, affliction is something quite apart, specific and irreducible.>
OUTPUT: <In the realm of suffering, affliction (o i wish mine enemies would volunteer themselves into rancid pink pink pink smoothies) is something quite apart, specific and irreducible.>

INPUT:<%s>
OUTPUT:<"""

