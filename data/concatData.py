# -*- coding: UTF-8 -*-

import csv
from random import random

RATE = 0.85

# input: file_address (test.csv)
# output: list of tuple
#			tuple: (order_number, stn)  (str, str)
def readTrain(file_address):
	csv_file = file(file_address, 'rb')
	reader = csv.reader(csv_file)
	reader = list(reader)
	csv_file.close()
	for stn in reader:
		if stn:
			yield tuple(stn[0].split('\t'))

def readLabel(file_address):
	csv_file = file(file_address, 'rb')
	reader = csv.reader(csv_file)
	reader = list(reader)
	csv_file.close()
	stns = [tuple(stn[0].split('\t')) for stn in reader if stn is not []]
	return stns


def writeCsv(file_address, result, isTrain = True):
	csv_file = file(file_address, 'wb')
	writer = csv.writer(csv_file)
	if isTrain:
		writer.writerow(['SentenceId', 'View', 'Opinion'])
	else:
		writer.writerow(['SentenceId', 'Content'])
	writer.writerows(result)
	csv_file.close()


def concatData(rate):
	cross_test_set = []
	cross_test_label_set = []
	pure_training_set = []
	pure_training_label_set = []

	train_first = readTrain('dataFirst/TrainFirst.csv')
	label_first = readLabel('dataFirst/LabelFirst.csv')
	for x in train_first:
		x_id = x[0]
		x_labels = [label for label in label_first if label[0] == x_id]
		if random() <= rate:	# has 'rate' probability to push it into pure_training_set
			pure_training_set.append(x)
			pure_training_label_set += x_labels
		else:
			cross_test_set.append(x)
			cross_test_label_set += x_labels

	# same process in second data set, yet I am too lazy to abstract it as a function :)
	train_second = readTrain('dataSecond/TrainSecond.csv')
	label_second = readLabel('dataSecond/LabelSecond.csv')
	for x in train_second:
		x_id = x[0]
		x_labels = [label for label in label_second if label[0] == x_id]
		if random() <= rate:	# has 'rate' probability to push it into pure_training_set
			pure_training_set.append(x)
			pure_training_label_set += x_labels
		else:
			cross_test_set.append(x)
			cross_test_label_set += x_labels


	# write data set into csv
	writeCsv('dataConcat/TrainConcat.csv',pure_training_set)
	writeCsv('dataConcat/LabelConcat.csv',pure_training_label_set, isTrain=False)
	writeCsv('dataConcat/CrossTest.csv',cross_test_set)
	writeCsv('dataConcat/CrossTestLabel.csv',cross_test_label_set, isTrain=False)
	print('Yes!')

if __name__	== '__main__':
	concatData(RATE)
