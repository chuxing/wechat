#######################################################  
#File Name: remove_repeat_data.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-06-16 17:55:37
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    frname1 = sys.argv[1]
    frname2 = sys.argv[2]
    fwname = sys.argv[3]
    fr1 = codecs.open(frname1,'r','gb2312', errors = 'ignore')
    fr2 = codecs.open(frname2,'r','gb2312', errors = 'ignore')
    fw = codecs.open(fwname,'w','gb2312')
    testset = set()
    for line in fr1.readlines():
        testset.add("".join(line.split(" ")[1:]).strip("\r\n"))
    for line in fr2.readlines():
        sentence = "".join(line.split(" ")[1:]).strip("\r\n")
        if sentence in testset:
            continue
        fw.write(line)


