#######################################################  
#File Name: getfasttextdata.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-07-03 19:10:42
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    frname = sys.argv[1]
    #fwname = sys.argv[2]
    fw = codecs.open(frname + "_new", 'w','gb18030')
    for line in codecs.open(frname,'r','gb18030', errors = 'ignore'):
        linesplit = line.split(" ")
        sentence = linesplit[0]
        tmps = "".join(linesplit[1:])
        for tmpi in tmps:
            sentence += " "+ tmpi
        fw.write(sentence)

            
