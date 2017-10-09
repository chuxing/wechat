import os
import codecs
import sys
if __name__ == '__main__':
	directory = sys.argv[1]
	rootdir = "./" + directory
	files = os.listdir(rootdir)
	for file in files:
		path = os.path.join(rootdir, file)
		f = codecs.open(path,'r','gb2312',errors='ignore')
		filew = "row_" + file 
		pathw = os.path.join(rootdir,filew)
		fw = codecs.open(pathw,'a','gb2312')
		for line in f.readlines():
			sentence = "".join(line.split(" ")[1:])
			fw.write(sentence)
