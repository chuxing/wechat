#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: rand_k_valid.py
# Author: 
# Mail: @.com
# Created Time: Tue 21 Mar 2017 10:58:57 AM CST
#########################################################################
import sys, random

for line in open(sys.argv[1]):
    number = int(sys.argv[2])                                                                                                                                                            
    idx = int(random.random() * number)
    #id  = int(random.random() * 10)
    print str(idx) + "\t" + line.strip()



