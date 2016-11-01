

import pycrfsuite

# do the sentiment analysis job
# input: tokens (list)
#        address (dict)
# output: result (dict)
#			key: entity_name (str)
#			value: label (str) (pos or neg)

def crf(tokens, address):



	#features 
	def word2features(sent, word):
		for word in sent:
			features = [ 
			'U00:' + address[word], 
			'U01:' + address[word - 1], 
			'U02:' + address[word + 1]
			]
		return features

	def sent2features(sent):
		return [word2features(sent, word) for word in sent]

	def sent2labels(sent):
		return [address[word] for word in sent]


	
	X_train = [sent2features(stn) for stn in readCsv(Train.csv)] 
	y_train = [sent2labels(stn) for stn in readCsv(Train.csv)]

	X_test = [sent2features(stn) for stn in readCsv(Test.csv)] 
	y_text = [sent2labels(stn) for stn in readCsv(Test.csv)]
	
	


	#train the model
	trainer = pycrfsuite.Trainer(verbose=False)

	for xseq, yseq in zip(X_train, y_train):
		trainer.append(xseq, yseq)

	trainer.set_params({
    	'c1': 1.0,   # coefficient for L1 penalty
    	'c2': 1e-3,  # coefficient for L2 penalty
    	'max_iterations': 50,  # stop earlier

	    # include transitions that are possible, but not observed
		'feature.possible_transitions': True
	})

	trainer.train('Train.csv')

	!ls -lh ./Train.csv


	#make predictions
	tagger = pycrfsuite.Tagger()
	tagger.open('Train.csv')

# output: result (dict)
#			key: entity_name (str)
#			value: label (str) (pos or neg)	
	result = dict()
	for i in result:
		i = address.key(i)
		result[i] = tagger.tag(sent2features(tokens))

	labels = [result[key] for key in result]


	return labels









