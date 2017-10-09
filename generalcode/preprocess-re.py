#coding:utf-8
import os
import codecs
import jieba
import thulac
def getrawfile():
	newfilename = 'D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_raw_data_all.txt'
	fraw = codecs.open("D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_reminder_all.txt","rb",'gb18030', errors = 'ignore')
	if os.path.exists(newfilename):
		os.remove(newfilename)
	frawout = codecs.open(newfilename,"a",'utf-8')
	for line in fraw.readlines():
		sentence = line
		# sentence = sentence.strip()
		# sentence = unicode(sentence)
		sentencesplit = sentence.split(" ")
		sentence = sentencesplit[0] + " "
		for _ in sentencesplit[1:]:
			sentence += _
		frawout.write(sentence)
def getvalidfile():
	newfilename = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_raw_data_balance.txt"
	fraw = codecs.open("D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_reminder_balance.txt","rb",'gb18030', errors = 'ignore')
	if os.path.exists(newfilename):
		os.remove(newfilename)
	frawout = codecs.open(newfilename,"a",'utf-8')
	for line in fraw.readlines():
		sentence = line
		sentencesplit = sentence.split(" ")
		sentence = sentencesplit[0] + " "
		for _ in sentencesplit[1:]:
			sentence += _
		frawout.write(sentence)
# 判断一个unicode是否是汉字
def is_chinese(uchar):         
    if u'\u4e00' <= uchar<=u'\u9fff':
        return True
    else:
        return False

# 判断一个unicode是否是数字
def is_number(uchar):
    if u'\u0030' <= uchar  and uchar <= u'\u0039':
        return True
    else:
        return False

# 判断一个unicode是否是英文字母
def is_alphabet(uchar):         
    if (u'\u0041' <= uchar<=u'\u005a') or (u'\u0061' <= uchar<=u'\u007a'):
        return True
    else:
        return False
def dojiebacut(fopen,frawout):
	# print fopen
	for rawsentence in fopen.readlines():
		newsentence = ""
		sentencesplit = rawsentence.split(" ")
		newsentence += (sentencesplit[0])
		sentence = ""
		for tmpi in sentencesplit[1:]: sentence+=tmpi
		# print sentence
		seg_list = jieba.cut(sentence)
		cnt = 0
		for i in seg_list:
			# if cnt < 7:
			# 	newsentence += i
			# else:
			# 	if cnt == 7:
			# 		newsentence = newsentence.rstrip()
			# if not is_chinese(i[0]):
			# 	for item in i:
			# 		newsentence += (" " + item)
			# else:
			newsentence += (" " + i)  
			cnt += 1
		# print newsentence
		frawout.write(newsentence)
		# print (" ".join(seg_list))
def jiebacut(name):
	rawfilename = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_" + name + ".txt"
	fopen = codecs.open(rawfilename,"r",'utf-8')
	newfilename = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_jieba_" + name + ".txt"
	if os.path.exists(newfilename):
		os.remove(newfilename)
	frawout = codecs.open(newfilename,"a",'utf-8')
	dojiebacut(fopen,frawout)
	fopen.close()
	frawout.close()
	
def dothucut(fopen,frawout):
	thu = thulac.thulac(seg_only=True)
	for sentence in fopen.readlines()[:5]:
		print sentence
		print thu.cut_f(sentence)

def thucut(name):
	rawfilename = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_" + name + ".txt"
	fopen = codecs.open(rawfilename,"r",'utf-8')
	newfilename = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_thu_" + name + ".txt"
	if os.path.exists(newfilename):
		os.remove(newfilename)
	frawout = codecs.open(newfilename,"a",'utf-8')
	dothucut(fopen,frawout)
	fopen.close()
	frawout.close()
if __name__ == '__main__':
	# getrawfile()
	# getvalidfile()
	# jiebacut("raw_data")
	# print "jiebarawdata done"
	# jiebacut("valid_data")
	# print "jiebavaliddata done"
	# thucut("raw_data")
	# print "thucutrawdata done"
	# thucut("valid_data")
	# print "thucutvaliddata done"

	jiebacut("raw_data_all")
	print "jiebarawdata done"
	jiebacut("raw_data_balance")
	print "jiebavaliddata done"
	jiebacut("valid_data_all")
	print "jiebarawdata done"
	jiebacut("valid_data_balance")
	print "jiebavaliddata done"


