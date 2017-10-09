#!/usr/bin/env python
# -*- coding:utf-8 -*-
#########################################################################
# File Name: record_confilts.py
# Author: 
# Mail: @.com
# Created Time: Tue 21 Mar 2017 11:24:52 AM CST
#########################################################################
import sys

if len(sys.argv) < 5:
    print "%s pred_result  raw_data  raw_data_flip_label"
    exit()

pred = sys.argv[1]
raw = sys.argv[2]
raw_flip = sys.argv[3]
data_dir = sys.argv[5]

pred_data = [line.strip() for line in open(pred)]
labels = {}
for idx, label in enumerate(pred_data[0].strip().split(" ")):
    labels[label] = idx
pred_data = pred_data[1:]

raw_data = [line.strip() for line in open(raw)]

sout_flip = open(raw_flip, "a")
sout_conflict = open(data_dir + "/record_flip_label_data.txt.v" + sys.argv[4], "a")

changed = 0

#print pred,raw,raw_flip,sout_flip
#print labels
for pred, raw in zip(pred_data, raw_data):
    pred_label = pred.split(" ")[0]
    pred_weights = [float(w) for w in pred.split(" ")[1:]]
    label = raw.split(" ")[0]
    if label not in labels or len(pred_weights) < len(labels):
        continue

    if pred_weights[labels[label]] < 0.1:
        changed += 1
        print >> sout_conflict, "R:" + label + "\tP:" + pred_label + "\t" + " ".join(raw.split(" ")[1:])
        label = pred_label
    print >> sout_flip, label + " " + " ".join(raw.split(" ")[1:])

print changed
sout_flip.close()
