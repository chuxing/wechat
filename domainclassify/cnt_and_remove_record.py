#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: cnt_and_remove_record.py
# Author: 
# Mail: @.com
# Created Time: Fri 24 Mar 2017 04:07:06 PM CST
#########################################################################
import sys

## 读入记录中被更改过标签的数据
## 删除原始数据中，标签被修改过的数据
## 新文件用.s结尾


if len(sys.argv) < 3:
    print "%s record_flip_label_data raw_data"
    exit()

record_datas = {}

sout = open(sys.argv[1]+"_s", "w")
for data in open(sys.argv[1]):
    parts = data.strip().split("\t")
    if len(parts) < 3:
        continue
    label = parts[1][2:]
    text = "".join(parts[2].split(" "))

    if text not in record_datas:
        record_datas[text] = {}

    if label not in record_datas[text]:
        record_datas[text][label] = 0

    record_datas[text][label] += 1

for key in record_datas:
    text = ""
    for label in record_datas[key]:
        text += label + "\t" + str(record_datas[key][label]) + "\t"
    print >> sout, text + "\t" + key
sout.close()

sout = open(sys.argv[2]+"_s", "w")  
for data in open(sys.argv[2]):
    parts = data.strip().split(" ")  
    label = parts[0]  
    text = "".join(parts[1:])  

    if text in record_datas:
        continue

    print >> sout, data.strip()
