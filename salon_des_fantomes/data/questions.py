import os.path as path
text_file_path = path.dirname(path.abspath(__file__)) + '/questions.txt'


with open(text_file_path,'r') as f:
	questions = [q.rstrip("\n") for q in f.readlines()]
