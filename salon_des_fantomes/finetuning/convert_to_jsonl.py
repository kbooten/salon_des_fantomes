import re





def main():
	file = 'answer_questions.txt'
	with open('answer_questions.txt','r') as f:
		data = f.read()
	pairs = re.split(r"\n{2,}",data)
	pairs = [re.split(r"\n",p) for p in pairs]
	pairs = [(a.strip(),q.strip()) for q,a in pairs] ## cleaning
	pairs = [(" "+a+"%%%"," "+q+"|||") for q,a in pairs] ## adding special characters to help model
	pairs = [(a.replace('"','\\"'),q.replace('"','\\"')) for a,q in pairs] ## adding special characters to help moded
	filestub = file.split(".")[0]
	first = True
	with open(filestub+".jsonl",'w') as outputfile:
		for a,q in pairs:
			if first==True: ## don't add a first newline
				first=False
			else:
				outputfile.write("\n")
			outputfile.write('{"prompt": "%s", "completion": "%s"}' % (a,q))








if __name__ == '__main__':
	main()