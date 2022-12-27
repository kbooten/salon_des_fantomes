prompt = """These are some monosyllabic words: "dog," "trounce," and "orc."

These are some words that aren't monosyllabic: "happy", "puppy", "wouldn't," and "harmony."

I want you to transform the input text in the following way.  Replace a single noun, verb, proper noun, or adjective in the input text with two very common monosyllabic (one-syllable) words, hyphenated.  One word should become two.  This transformation is called a "simplification-hypthenation."

Here is an example of what I want:

INPUT: <The forest was filled with elves.
OUTPUT: <The green-tall was filled with elves.

Notice that one word---"forest"---became two one-syllable words---"green-tall." And a forest is both green and tall, so calling a forest a "green-tall" makes sense.

Here is an example of what NOT to do:

INPUT: <The forest was filled with elves.
OUTPUT: <The upper-leafing was filled with elves.

This is WRONG because both words ("upper" and "leafing") are two-syllable words, not one-syllable words as they should be.

Here's another correct example of what I'm looking for:

INPUT: <I went to my car.>
OUTPUT: <I went to my wheel-box.>

Notice that one word---"car"---became two one-syllable  words---"wheel-box."  And a car is sort of a "wheel-box" because it is a container with wheels, so this "simplification-hypthenation" makes sense.

If the input text already has a "simplification-hyphenation," you can either transform another word like this:

INPUT: <I went to my wheel-box.>
OUTPUT: <I straight-swooped to my wheel-box.>

But you can also transform a "simplification-hyphenation" that is already in the input text:

INPUT: <I went to my wheel-box.>
OUTPUT: <I went to my wheel-square-cave.>

Now complete this one. And, remember, the general format of a simplification-hyphenation is "A-B" where A and B are both single-syllable words, not any more syllables than that.

INPUT:<%s>
OUTPUT:<"""