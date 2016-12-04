import jieba

#add car product's names in the Label.csv to the dict
def addword(file_address):
	LABELS = readCsv(file_address)
	for row in LABELS:
		add_word(row[1])

def readCsv(file_address):
	csv_file = file(file_address, 'rb')
	reader = csv.reader(csv_file)
	reader = list(reader)
	stns = [tuple(stn[0].split('\t')) for stn in reader if stn is not []]
	csv_file.close()
	return stns



def jbSeg(stn):
	addword('data/Label.csv')
	seg_list = jieba.cut(stn)
	seg_reallist = []
	for i in seg_list:
		seg_reallist.append(n)
	return seg_reallist


