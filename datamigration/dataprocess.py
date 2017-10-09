 # -*- coding:gb2312 -*- 
import codecs
import os
import sys
import re
def write2file(fileid,string):
	# print fileid,type(string)
	filename = "E:\\code\\datamigration\\rawtable\\rawtable" + fileid + ".txt"
	# if os.path.exists(filename):os.remove(filename)
	f = codecs.open(filename,'a','utf8')
	# print string,type(string)
	f.write(string + "\r\n")
def readfromfile():
	filename = "E:\\code\\data\\music.txt"
	f = codecs.open(filename,'r','gb18030')
	pattern1 = re.compile(r'\{.*\}')
	pattern2 = re.compile(r'\[.*\]')
	pattern3 = re.compile(r'\(.*\)')
	pattern4 = re.compile(r'\^.*\_') 
	pattern5 = re.compile(r'\@.*\#')
	pattern6 = re.compile(r'\$.*\%')
	pattern7 = re.compile(r'\&.*\*')
	table = [set() for _ in range(7)]
	for line in f.readlines():
		sentence = line[:-2]
		# print sentence
		match1 = pattern1.search(sentence)
		match2 = pattern2.search(sentence)
		match3 = pattern3.search(sentence)
		match4 = pattern4.search(sentence)
		match5 = pattern5.search(sentence)
		match6 = pattern6.search(sentence)
		match7 = pattern7.search(sentence)
		if match1:
   			# print match1.group()
   			table[0].add(match1.group()[1:-1])
   		if match2:
   			# print match2.group()
   			table[1].add(match2.group()[1:-1])
   		if match3:
   			# print match3.group()  
   			table[2].add(match3.group()[1:-1])
   		if match4:
   			# print match4.group() 
   			table[3].add(match4.group()[1:-1]) 
   		if match5:
   			# print match5.group()  
   			table[4].add(match5.group()[1:-1])
   		if match6:
   			# print match6.group()  
   			table[5].add(match6.group()[1:-1])
   		if match7:
   			# print match7.group()  
   			table[6].add(match7.group()[1:-1])
   	return table
	
if __name__ == '__main__':
	
	pattern = [line.strip() for line in codecs.open("pattern.txt", "r", "gb18030")]
	filename = "E:\\code\\datamigration\\query\\query4.txt"
	f = codecs.open(filename,'a','gb18030')
	for line in codecs.open("E:\\code\\data\\music.txt",'r','gbk').readlines():
		# print type(line)
		sentence = line
		for i in pattern:
			sentence = sentence.replace(i,'')
		# print sentence,type(sentence)
		try:
			f.write(sentence.encode('gb18030'))
		except Exception as e:
			print sentence
		# print sentence
	# rawtable = readfromfile()
	# for tablei in range(len(rawtable)):
	# 	# print rawtable[tablei]
	# 	for words in rawtable[tablei]:
	# 		# print words
	# 		flag = True
	# 		if words == '':continue
	# 		for i in pattern:
	# 			if i in words:
	# 				flag = False
	# 				break
	# 		if flag == True:
	# 			pass
				# print words+"asdf",type(words)
				# write2file(str(tablei+1), words)
