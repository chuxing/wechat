#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: create_corpus.py
# Author: 
# Mail: @.com
# Created Time: Tue 21 Mar 2017 11:03:04 AM CST
#########################################################################
import sys

idx = int(sys.argv[1])
data_dir = sys.argv[3]

sout_train = open(data_dir + "/train.txt", "w+")
sout_test  = open(data_dir + "/test.txt", "w+")

for line in open(sys.argv[2]):
    parts = line.strip().split("\t")
    valid = int(parts[0])
    text = parts[1]

    if valid == idx:
        print >> sout_test, text
    else:
        print >> sout_train, text


sout_test.close()
sout_train.close()
