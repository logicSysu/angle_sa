

def fetchDict(file_address):
	pf = open(file_address,'r')
	named_entites = list(pf)
	named_entites = [x[:-1] for x in named_entites]	# remove the last \n
	pf.close()
	return named_entites

def naiveNer(tokens):
	named_entites = fetchDict('data/View.txt')
	address = {}
	for token in tokens:
		if token in named_entites:
			address[token] = tokens.index(token)
	return address
