#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: ana_error.py
# Author: 
# Mail: @.com
# Created Time: Fri 19 May 2017 10:48:52 AM CST
#########################################################################
import sys, codecs

golden = [line.strip() for line in codecs.open(sys.argv[1], "r", "gb18030")]
predict = [line.strip() for line in codecs.open(sys.argv[2], "r" , "gb18030")]
predict = predict[1:]
out_file = codecs.open(sys.argv[3], "w+", "gb18030")

for line1, line2 in zip(golden, predict):
  golden_label = line1.split(" ")[0]
  predict_label = line2.split(" ")[0]
  query = " ".join(line1.split(" ")[1:])
  if golden_label != predict_label:
    out_file.write("p: " + predict_label + " g: " + golden_label + " " + query + "\n")

out_file.close()
