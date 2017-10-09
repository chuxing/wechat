#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: random_split.py
# Author: letian
# Mail: @.com
# Created Time: Mon 08 May 2017 03:33:24 PM CST
#########################################################################
import sys, random
import codecs
ratio = float(sys.argv[2])

file1 = codecs.open(sys.argv[1] + "_" + str(ratio), "w+",'gb18030')
file2 = codecs.open(sys.argv[1] + "_" + str(1 - ratio), "w+","gb18030")

for line in codecs.open(sys.argv[1],'r','gb18030',errors = 'ignore'):
  line = line.strip() + "\n"
  if random.random() < ratio:
    file1.write(line)
  else:
    file2.write(line)

file1.close()
file2.close()
