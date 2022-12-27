import gpt_interface

from dotenv import load_dotenv
import os
load_dotenv('.env') 
a2q_model = os.environ.get("a2q_model")

def get_question_about_statement(statement,prompt_suffix="%%%",completion_suffix="|||"):
	prompt = " %s%s" % (statement,prompt_suffix)
	question = gpt_interface.gpt3_from_prompt(prompt,model=a2q_model,stop=completion_suffix)
	question.rstrip(completion_suffix)
	return question

def main():
	statement = "Based on making people more engaged with their body and their space, I think that cars should be illegal."
	statement = "When Latvia took over the world, I respected that."
	
	print(get_question_about_statement(statement))

if __name__ == '__main__':
	main()

