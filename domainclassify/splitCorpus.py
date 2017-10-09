#!/usr/bin/env python
import os, sys, random

all_data = {}
if len(sys.argv)<5:
    print "python splitCorpus.py raw train test count"
    exit()

for line in open(sys.argv[1]):
    parts = line.strip("\r\t\n ").split(" ")
    text = " ".join(parts[1:])
    label = parts[0]

    if "__label__" not in label:
        continue
    
    if label not in all_data:
        all_data[label] = []

    all_data[label].append(label + " " + text)

sout_train = open(sys.argv[2], "w")
sout_test = open(sys.argv[3], "w")

for label, datas in all_data.items():
    testSize = min([len(datas) * 0.05, int(sys.argv[4])])
    testSize = max(1, testSize)
    print "%s, size=%d, test-size=%d" % (label, len(datas), testSize)
    random.shuffle(datas)
    for idx, line in enumerate(datas):
        try:
            line = line.decode("gb18030").encode("gb18030")
        except UnicodeEncodeError:
            continue
        r = random.random();
        if testSize > 0:
            print >> sout_test, line
            testSize -= 1 
        else:
            print >> sout_train, line

    
sout_test.close()
sout_train.close()
