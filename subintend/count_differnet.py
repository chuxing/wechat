#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: count_differnet.py
# Author: 
# Mail: @.com
# Created Time: Wed 29 Mar 2017 05:20:48 PM CST
#########################################################################
import sys, math


counts = {}
counts1 = {}

for filename in sys.argv[1:]:
    for line in open(filename):
        parts = line.strip().split(" ")
        label = parts[0]
        text = "".join(parts[1:])

        if "dianbo" in label:
            if text not in counts:
                counts[text] = 0
            counts[text] += 1
        else:
            if text not in counts1:
                counts1[text] = 0
            counts1[text] += 1
print len(counts), len(counts1)

diff = {}
for k in counts:
    if k not in counts1:
        diff[k] = counts[k]
        counts1[k] = 0
        continue
    time = abs(counts[k] - counts1[k])
    diff[k] = time

sortitems = sorted(diff.iteritems(), key=lambda x:x[1], reverse=False)

for k, v in sortitems:
    print "dianbo:" + str(counts[k]) + "\t" + "normal:" + str(counts1[k]) + "\t" + str(v) + "\t" + k


