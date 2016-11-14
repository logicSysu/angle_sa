# -*- coding: UTF-8 -*-

import pycrfsuite
import csv

import JiebaSeg as jb
import sentimenter as st

import thuSeg as seg




# input: file_address (test.csv)
# output: list of tuple
#			tuple: (order_number, stn)  (str, str)
def readCsv(file_address):
	csv_file = file(file_address, 'rb')
	reader = csv.reader(csv_file)
	reader = list(reader)
	stns = [tuple(stn[0].split('\t')) for stn in reader if stn is not []]
	csv_file.close()
	return stns

LABELS = readCsv('data/Label.csv')

#features 
# def word2features(sent, word):
# 	for word in sent:
# 		features = [ 
# 		'U00:' + address[word], 
# 		'U01:' + address[word - 1], 
# 		'U02:' + address[word + 1]
# 		]
# 	return features

# def sent2features(sent):
# 	return [word2features(sent, word) for word in sent]

# def sent2labels(sent):
# 	return [address[word] for word in sent]

def fetchLabelPair(stn_id):
	result_dict = {}
	for label in LABELS:
		if stn_id == label[0]:
			result_dict[label[1]] = label[2]
	return result_dict

def prettyStn(tokens, stn_id='0', is_train=True):
# '''
# merge the training stns with labels w.r.t. each tokens.
# input: stn (str); stn_id (str)
# output: list of triple (token, pos, label)
# for example,
# 	input "大众的车不错"
# 	output: [('大众', 'n', 'pos'),
# 			 ('车',   'n', 'O'),
# 			 ('不错', 'n', 'O')
# 			]
# '''
	str2triple = lambda token : token.split('_') + ['o']
	init_triples = [str2triple(token) for token in tokens]
	if is_train:
		labels = fetchLabelPair(stn_id)
		for i in range(len(init_triples)):
			triple = init_triples[i]
			#print 1111,triple
			for label in labels:
				if label.startswith(triple[0]):
					triple[0] = label
					# need to merge the duplicate tokens
					triple[2] = labels[label]
					if i > 0:
						if labels[label] == 'pos':
							init_triples[i-1][2] = 'b-pos'	# label as 'before pos'
						elif labels[label] == 'neg':
							init_triples[i-1][2] = 'b-neg'	# label as 'before neg'
						elif labels[label] == 'neu':
							init_triples[i-1][2] = 'b-neu'	# label as 'before neu'
	triples = [tuple(triple) for triple in init_triples if len(triple) == 3]
	#print triples
	return triples

#####  copy from example in http://nbviewer.jupyter.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    features += st.howManyAroundIt(sent, i, 6)	# detect how many negations, sentiment words around i, in the range of [i-6,i+6]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))] #+ st.numFeatures(sent)

def sent2labels(sent):
    #print 2222,sent
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]  


#####  copy from example in http://nbviewer.jupyter.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb



def trainModel(withDefaultTokens=True):

	if withDefaultTokens:
		pf = open('data/tokens.txt','r')
		train_sents = eval(pf.read())
	else:
		raw_train_sents = readCsv('data/Train.csv')
		train_sents = [prettyStn(seg.segmenter(stn), stn_id) for stn_id, stn in raw_train_sents]
		#train_sents = [prettyStn(jb.jbSeg(stn), stn_id) for stn_id, stn in raw_train_sents]

	X_train = [sent2features(s) for s in train_sents]
	y_train = [sent2labels(s) for s in train_sents]
	#print y_train

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

	trainer.train('data/cfrModel_withSent.crfsuite')

#	!ls -lh ./Train.csv



# do the sentiment analysis job
# input: tokens (list)
#        address (dict)
# output: result (dict)
#			key: entity_name (str)
#			value: label (str) (pos or neg)

def crf(tokens):

	#make predictions
	tagger = pycrfsuite.Tagger()
	tagger.open('data/cfrModel_withSent.crfsuite')
	raw_tokens = prettyStn(tokens,'0',False)	# need to o
	labels = tagger.tag(sent2features(raw_tokens))
	#print labels
	result = {}
	for i in range(len(labels)):
		if labels[i] == 'neu' or labels[i] == 'pos' or labels[i] == 'neg':
			result[raw_tokens[i][0]] = labels[i]
	return result









