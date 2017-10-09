 # -*- coding:utf8 -*- 
import os
import linecache
import random
import codecs
class FileProcess(object):
	"""docstring for FileProcess"""
	def __init__(self):
		super(FileProcess, self).__init__()
		
	def write2file(self,domian,flag,fileid,method,string):
		filename = "./" + domian + "/newdomain/newdomain_" + method + fileid + ".txt"
		if flag == 1 and os.path.exists(filename):os.remove(filename)
		f = codecs.open(filename,'a','gb2312')
		f.write(string.decode('utf8') + "\n")
	def readfromfile(self,domain,fileid,linecnt):
		filename = "./" + domain + "/newtable/newtable_" +  fileid + ".txt"
		f = codecs.open(filename,'r','gb2312')
		tmpstr = ""
		# print linecnt,randomline
		# print filename
		try:
			randomline = random.randrange(1,linecnt + 1)
			tmpstr =  (linecache.getline(filename,randomline).decode('gb2312').encode('utf8')).rstrip("\n")
			# tmpstr = 
		except Exception as e:
			pass
			# print "read error"
		# print tmpstr+"sdf"
		return tmpstr
