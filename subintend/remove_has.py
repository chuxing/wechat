#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: remove_has.py
# Author: 
# Mail: @.com
# Created Time: Mon 27 Mar 2017 11:35:55 PM CST
#########################################################################
import sys

datas =set( [data.strip().split("\t")[1] for data in open(sys.argv[1])])

sout = open(sys.argv[3] + ".in", "w")
sout_not_in = open(sys.argv[3] + ".notin", "w")

for data in open(sys.argv[2]):
    text = data.strip().split("\t")[0]
    if text in datas:
        print >> sout, text
    else:
        print >> sout_not_in, text
sout.close()
sout_not_in.close()

