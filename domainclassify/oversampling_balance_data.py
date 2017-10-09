#!/usr/bin/env python
#-*- coding:gb18030 -*-


"""
������������ݵ���Ϊ�������ݣ�
������������
���룬label data
�����label data
"""

import sys,math,random


if len(sys.argv) < 3:
    print "python oversampling_balance_data.py input output"
    exit()

label_datas = {}

for data in open(sys.argv[1]):
    parts = data.strip().split(" ")
    if len(parts) < 2:
        continue
    label = parts[0]
    if label not in label_datas:
        label_datas[label] = []
    label_datas[label].append(data.strip())

m = max([len(label_datas[x]) for x in label_datas.keys()]) / 10
print m

sout = open(sys.argv[2], "w")

for label in label_datas:
    datas = label_datas[label]

    print >> sout, "\n".join(datas)

    # ��������������������ȫ
    for i in range(len(datas), m):
        print >> sout, random.choice(datas)

sout.close()
