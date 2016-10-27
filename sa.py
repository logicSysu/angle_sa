# -*- coding: UTF-8 -*-

import csv
import myCrf
import thuSeg
import myRec


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
	tokens_dict = myRec.recognizer(tokens)
	labels = myCrf.crf(tokens, tokens_dict)
	return labels


def writeLabels(file_address, labels):
	csv_file = file(file_address, 'wb')
	writer = csv.writer(csv_file)
	writer.write(labels)	# need to refine
	csv_file.close()


def main():
	stns = readCsv('data/Test.csv')
	for stn_pair in stns:
		stn_num = stn_pair[0]
		stn = stn_pair[1]
		labels = sentimenter(stn)
		writeLabels(labels)
	print "Yes!"




if __name__ == "__main__":
	main()
	
	
