#!/usr/bin/python  
#-*- coding:utf-8 -*-  
#######################################################  
#File Name: getlengtg.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-07-12 19:58:07
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
    fr = codecs.open(frname,'r','gb18030',)
    fw = codecs.open("long.out",'w','gb18030')
    fw2 = codecs.open("shorttrain",'w','gb18030')
    for line in fr.readlines():
        leng = len(line.split(" ")) - 1
        if leng > 30:
            fw.write(line)
        else:
            fw2.write(line)
