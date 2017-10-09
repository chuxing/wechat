#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: record_errors.py
# Author: Chu Xing
# Mail: v_xingzhu@.tencentcom
# Created Time: Fri 16 Jun 2017 17:31:52 PM CST
#########################################################################
import sys
import os
#if len(sys.argv) < 5:
    #print "%s pred_result  raw_data  raw_data_flip_label"
    #exit()

pred = sys.argv[1]
raw = sys.argv[2]

pred_data = [line.strip() for line in open(pred)]
labels = {}
for idx, label in enumerate(pred_data[0].strip().split(" ")):
    labels[label] = idx
pred_data = pred_data[1:]

raw_data = [line.strip() for line in open(raw)]

if os.path.exists("record_flip_label_data.txt"): os.remove("record_flip_label_data.txt")
sout_conflict = open("record_flip_label_data.txt", "a")

errors = 0

#print pred,raw,raw_flip,sout_flip
#print labels
for pred, raw in zip(pred_data, raw_data):
    pred_label = pred.split(" ")[0]
    pred_weights = [float(w) for w in pred.split(" ")[1:]]
    label = raw.split(" ")[0]
    if label not in labels or len(pred_weights) < len(labels):
        continue

    if pred_label != label:
        errors += 1
        print >> sout_conflict, "R:" + label + "\tP:" + pred_label + "\t" + " ".join(raw.split(" ")[1:]) + str(pred_weights)

print errors
