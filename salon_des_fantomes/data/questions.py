import random
import os.path as path
text_file_path = path.dirname(path.abspath(__file__)) + '/questions.txt'

with open(text_file_path,'r') as f:
	questions = [q.rstrip("\n") for q in f.readlines()]

text_file_path2 = path.dirname(path.abspath(__file__)) + '/art.txt'
# with open(text_file_path2,'r') as f:
# 	art = [q.rstrip("\n") for q in f.readlines()]

# art_questions_templates = [
# 	"Just over there we see %s?  What does it mean? Do you admire it?  Why or why not?",
# 	"Above us we can see %s?  How should we make sense of this work?",
# 	"Above us we can see %s?  Do you like it?  Would you want it in your living room?",
# 	"Above us we can see %s?  What is the function of this artwork?",
# ]

# for a in art:
# 	template = random.choice(art_questions_templates)
# 	questions.append(template % a)

# random.shuffle(questions)
