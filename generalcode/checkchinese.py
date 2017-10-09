#######################################################  
#File Name: checkchinese.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-06-15 12:12:10
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
class checkChinese(object):
    def __init__(self,uchar):
        super(checkChinese, self).__init__()
        self.uchar = uchar

    def is_chinese(self):         
        if u'\u4e00' <= self.uchar<=u'\u9fff':
            return True
        else:
            return False

    def is_number(self):
        if u'\u0030' <= self.uchar  and self.uchar <= u'\u0039':
            return True
        else:
            return False

    def is_alphabet(self):         
        if (u'\u0041' <= self.uchar<=u'\u005a') or (u'\u0061' <= self.uchar<=u'\u007a'):
            return True
        else:
            return False
