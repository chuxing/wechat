#!/usr/bin/env python

import os, sys

"""
    python viewResult.py real predict
"""

sin = open(sys.argv[1])
realLabels = [x.strip().split(" ")[0] for x in sin]
sin = open(sys.argv[2])
predLabels = [x.strip().split(" ")[0] for x in sin]
sin = open(sys.argv[2])   
line = sin.readline()
if len(line.split("__label__")) > 2:
    print "Fasttext Result"
    predLabels = predLabels[1:]

labels = set(realLabels) | set(predLabels)

confuseMatrix = {}
for label in labels:
    confuseMatrix[label] = {}
    for _label in labels:
        confuseMatrix[label][_label] = 0.    

for real,pred in zip(realLabels, predLabels):
    confuseMatrix[real][pred] += 1.

# row is real, column is prediction

print "> "+sys.argv[1].split("/")[-1].split(".")[0]

print "> Label  Precision  Recall  F-value  Total  Predict  Correct"
ps, rs, fs = [], [], []
labels_list = list(labels)
labels_list.sort()

for label in labels:
    if label.find("n/a") != -1:
      continue
    realtotal = sum(confuseMatrix[label].values())
    predtotal = sum(confuseMatrix[_][label] for _ in labels)
    p, r, f  = 0., 0., 0.
    if realtotal != 0:
        r = confuseMatrix[label][label] / realtotal
    if predtotal != 0:
        p = confuseMatrix[label][label] / predtotal
    if p != 0 or r != 0:
        f = (p * r * 2) / (p + r)
    print "%s  %f  %f  %f  Toal=%d  Pred=%d  Corr=%d" % (label, p, r, f, realtotal, predtotal, confuseMatrix[label][label])
    ps.append(p)
    rs.append(r)
    fs.append(f)

if len(labels) < 10:
    print "> Row(real), Column(predict)"
    for rowLabel in labels:
        if rowLabel.find("n/a") != -1:
            continue
        print "",
        for columnLabel in labels:
            if columnLabel.find("n/a") != -1:
                continue
            print str(confuseMatrix[rowLabel][columnLabel]) + "\t",
        print 

totalCorrec = 0.
for label in labels:
  if label.find("n/a") != -1:
    continue
  totalCorrec += confuseMatrix[label][label]
print "Total Correct: %d/%d=%f  %f  %f  %f" % (totalCorrec, len(realLabels), totalCorrec/len(realLabels), sum(ps)/len(ps), sum(rs)/len(rs), sum(fs)/len(fs))
# print totalCorrec/len(realLabels)
print "\n\n"
