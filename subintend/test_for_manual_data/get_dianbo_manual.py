#######################################################  
#File Name: get_dianbo_manual.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-06-20 15:49:24
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
    fwname = sys.argv[2]
    fr = codecs.open(frname,'r','gb2312',errors = 'ignore')
    fw = codecs.open(fwname,'w','gb2312')
    dataset = set()
    for line in fr.readlines():
        dataset.add(line)
    for item in dataset:
        fw.write(item)
