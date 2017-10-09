# -*- coding:utf8 -*-
import os
import codecs
import random
import linecache
import sys
from PatternMatch import PatternMatch


def getData(rootdir,flag = 0):
    datalist = []
    labellist = []
    files = os.listdir(rootdir)
    ids = str(files[0]).index('_')
    files.sort(key= lambda x:int(x[ids+1:-4]))
    for file in files:
        data = []
        label = []
        path = os.path.join(rootdir, file)
        #print path
        f = codecs.open(path, "r", 'gb2312', errors='ignore')
        for line in f.readlines()[:]:
            if flag == 0:
                data.append(line.strip("\r\n"))
            else:
                label.append(line.strip().split(" ")[0])
                data.append("".join(line.strip().split(" ")[1:]))
        datalist.append(data)
        labellist.append(label)
    if flag == 0:
        return datalist 
    else:
        return labellist,datalist


if __name__ == '__main__':
    domain_name = sys.argv[1]
    generate_number_for_each_sentence = int(sys.argv[2])
    prestring = "./" + domain_name
    querylabellist,querylist = getData(prestring + "/query/",1)
    rawtable = getData(prestring + "/rawtable/")
    newtable = getData(prestring + "/newtable/")
    print "read done"
    pm = PatternMatch(querylist, rawtable, newtable,querylabellist)
    print "init done"
    pm.rawtableProcess()
    print "trie done"
    pm.matchQuery()
    print "mathch done"
    pm.genNewdomain(domain_name, generate_number_for_each_sentence)
    print "generate done"
