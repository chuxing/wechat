#!/usr/bin/python  
#-*- coding:utf-8 -*-  
#######################################################  
#File Name: aa.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-07-21 09:31:55
########################################################  
from __future__ import unicode_literals
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Seven Chu'

if __name__ == '__main__':
    frname = sys.argv[1]
    fr = codecs.open(frname, 'r','gb18030')
    fw = codecs.open(frname + "_new",'w','gb18030')
    for line in fr.readlines():
        newsentence = "__label__music"
        for i in line:
            newsentence += " " + i
        fw.write(newsentence)
