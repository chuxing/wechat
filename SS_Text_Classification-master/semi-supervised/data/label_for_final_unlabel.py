#######################################################  
#File Name: label_for_final_unlabel.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-07-06 16:19:24
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    frunlablename = sys.argv[1]
    frunlable = codecs.open(frunlablename,'r','gb18030',errors = 'ignore')
    frlabelname = codecs.open(sys.argv[2],'r','gb18030',errors = 'ignore')
    fw = codecs.open(sys.argv[3],'w','gb18030')
    unlabelset = set()
    for line in frunlable.readlines():
        sentence = "".join(line.split(" ")).strip()
        unlabelset.add(sentence)
    for line in frlabelname.readlines():
        sentence = "".join(line.split(" ")[1:]).strip()
        if sentence in unlabelset:
            fw.write(line)

