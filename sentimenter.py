# -*- coding: UTF-8 -*-


# a file to a dictionary, which is a list of word
# input: file_address (str)
# output: dictionary (list)
def file2dict(file_address):
	pf = open(file_address,'r')
	dictionary = list(pf)
	return dictionary

negReviewWords = file2dict('情感词典/negReviewWord.txt')
negSentimentWords = file2dict('情感词典/negSentimentWord.txt') + file2dict('NTUSD/NTUSD_simplified/NTUSD_negative_simplified.txt')
posReviewWords = file2dict('情感词典/posReviewWord.txt')
posSentimentWords = file2dict('情感词典/posSentimentWord.txt') + file2dict('NTUSD/NTUSD_simplified/NTUSD_positive_simplified.txt')
negations = file2dict('情感词典/negation.txt')


def getTagFromDict(word):
	tag = ''
	if word in posSentimentWords:
		tag += '1'
	if word in posReviewWords:
		tag += '2'
	if word in negSentimentWords:
		tag += '3'
	if word in negReviewWords:
		tag += '4'
	if word in negations:
		tag += '5'
	return tag

def howManyAroundIt(sent, i, range=6):
	begin = max(0,i-range)
	end   = min(len(sent),i+range)
	area = sent[begin:end]
	num_of_negation = 0
	num_of_negReview = 0
	num_of_posReview = 0
	num_of_negSentiment = 0
	num_of_posSentiment = 0
	for word in area:
		if word in posSentimentWords:
			num_of_posSentiment += 1
		if word in posReviewWords:
			num_of_posReview += 1
		if word in negSentimentWords:
			num_of_negSentiment += 1
		if word in negReviewWords:
			num_of_negReview += 1
		if word in negations:
			num_of_negation += 1
	num_features = []
	if num_of_posSentiment:
		num_features.append('num.posSentiment='+str(num_of_posSentiment))
	if num_of_posReview:
		num_features.append('num.posReview='+str(num_of_posReview))
	if num_of_negSentiment:
		num_features.append('num.negSentiment='+str(num_of_negSentiment))
	if num_of_negReview:
		num_features.append('num.negReview='+str(num_of_negReview))
	if num_of_negation:
		num_features.append('num.negation='+str(num_of_negation))
	return num_features
	


def numFeatures(sent):
	d = dict()
	d[neg] = 0
	d[sentiment] = 0
	d[verb] = 0
	d[adv] = 0
	d[question] = 0
	d[exclamation] = 0
	temp = []
	dictlist = []
	for word in sent:
		if sent[word][1] == '''negatives''':
			d[neg] = d[neg] + 1
		elif sent[word][1] == '''sentiment words''':
			d[sentiment] = d[sentiment] + 1
		elif sent[word][1] == '''verb''':
			d[verb] = d[verb] + 1
		elif sent[word][1] == '''adv''':
			d[adv] = d[adv] + 1
		elif sent[word][1] == '''question words''':
			d[question] = d[question] + 1
		elif sent[word][1] == '''exclamation''':
			d[exclamation] = d[exclamation] + 1
	for key, value in d.iteritems():
		temp = [key + value]
		dictlist.append(temp)
	return dictlist