# -*- coding: UTF-8 -*-

import csv
import myCrf
import thuSeg
#import myRec
import naiveNer


# input: file_address (test.csv)
# output: list of tuple
#			tuple: (order_number, stn)  (str, str)
def readCsv(file_address):
	csv_file = file(file_address, 'rb')
	reader = csv.reader(csv_file)
	reader = list(reader)
	stns = [tuple(stn[0].split('\t')) for stn in reader]
	csv_file.close()
	return stns


# some preprocesing step for a sentence
# for example stemming and strip the puncuation
# input: raw_stn (str)
# output: stn (str)
def preprocessing(raw_stn):
	return raw_stn.strip()


# input: stn
# output: dict:
#			key: entity_name (str)
#			value: label (str) (pos or neg)
def sentimenter(stn):
	stn = preprocessing(stn)
	tokens = thuSeg.segmenter(stn)
	#tokens_dict = myRec.recognizer(tokens)
	#tokens_dict = naiveNer.naiveNer(tokens)
	labels = myCrf.crf(tokens)
	return labels


def writeLabels(file_address, result):
	csv_file = file(file_address, 'wb')
	writer = csv.writer(csv_file)
	writer.writerow(['SentenceId', 'View', 'Opinion'])
	writer.writerows(result)
	csv_file.close()


def main():
	stns = readCsv('data/Test.csv')
	result = []
	count = 0
	for stn_pair in stns:
		stn_num = stn_pair[0]
		stn = stn_pair[1]
		labels = sentimenter(stn)
		labels_stn_num = [tuple([str(stn_num), entity, labels[entity]]) for entity in labels]
		result += labels_stn_num
		count += 1
		print 'sentence '+str(count)+ ' finished. ' + str(count) + ' out of ' + str(len(stns))
	writeLabels('data/Answer.csv',result)
	print "Yes!"




if __name__ == "__main__":
	main()
	
	
