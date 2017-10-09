# -*- coding:utf8 -*-
import os
import codecs
import random
import linecache
import sys
from PatternMatch import PatternMatch


def getData(rootdir):
    datalist = []
    files = os.listdir(rootdir)
    ids = str(files[0]).index('_')
    files.sort(key= lambda x:int(x[ids+1:-4]))
    for file in files:
        data = []
        path = os.path.join(rootdir, file)
        print path
        f = codecs.open(path, "r", 'gb18030', errors='ignore')
        for line in f.readlines()[:]:
            data.append(line.strip("\r\n"))
        datalist.append(data)
    return datalist


def getData2(filename):
    f = codecs.open(filename, 'r', 'gb18030', errors = 'ignore')
    data = []
    for line in f.readlines():
        data.append(line.strip("\r\n"))
    return data

def word2pinyin(line):
    ns = ""
    for word in line.strip():
        if word in pinyindict:
            ns += pinyindict[word]
        else:
            ns += word 
    return ns

def getData3(rawfile,newfile,pinyindict):
    f1 = codecs.open(rawfile,'r','gb18030',errors = 'ignore')
    f2 = codecs.open(newfile,'w','gb18030',errors = 'ignore')
    data = []
    for line in f1.readlines():
        ns = word2pinyin(line)
        data.append(ns)
        f2.write(ns + "\n")
    return data

def do_fun(querylist,rawtablelist,dict_pattern_name,fwriter,wirtequerlist):
    print "read done"
    pm = PatternMatch(querylist, rawtablelist, dict_pattern_name)
    print "init done"
    pm.rawtableProcess()
    print "trie done"
    pm.matchQuery()
    print "mathch done"
    pm.genOutput(fwriter,wirtequerlist)

def combine_file(f1name,f2name,fwname):
    fw = codecs.open(fwname,'w','gb18030')
    for index,line in enumerate(codecs.open(f1name,'r','gb18030',errors = 'ignore')):
        ns = ""
        line2 = linecache.getline(f2name,index + 1)
        for tmps in line.strip().split("\t"):
            ns += tmps + "\t"
        for tmps in line2.strip().split("\t")[1:]:
            ns += tmps + "\t"
        ns = ns.strip() +  "\n"
        fw.write(ns)
    if os.path.exists(f1name):
        os.remove(f1name)
    if os.path.exists(f2name):
        os.remove(f2name)

if __name__ == '__main__':
    fquery = sys.argv[1]
    querylist_item = getData2(fquery)
    querylist = []
    querylist.append(querylist_item)
    fwriter = sys.argv[2]
    dict_pattern_name = {}
    pattern_cnt = -1
    rawtablelist = []
    pinyin_root = sys.argv[3] + "_pinyin"
    if not os.path.exists(pinyin_root):
        os.makedirs(pinyin_root)
    optargc = sys.argv[4]
    dict_pattern_name_pinyin = {}
    pinyindict = {}
    rawtablelist_pinyin = []
    for line in codecs.open("./pinyinModel.single",'r','gb18030').readlines():
        word = line.strip().split(" ")[0]
        pinyin = line.strip().split(" ")[1]
        pinyindict[word] = pinyin 
    fquery_pinyin = fquery.split(".")[0] + "_pinyin." + fquery.split(".")[1]
    querylist_item_pinyin = getData3(fquery,fquery_pinyin,pinyindict)
    querylist_pinyin = []
    querylist_pinyin.append(querylist_item_pinyin)
    for root, dirs, files in os.walk(sys.argv[3]):
      for f in files: 
        if not f.endswith("snt"):
          continue
        arg = os.path.join(root, f)
        pattern_cnt += 1
        rawtable = getData2(arg)
        rawtablelist.append(rawtable)
        dict_pattern_name[pattern_cnt] = arg.split("/")[-1].split(".")[0]
        arg2 = os.path.join(pinyin_root,f.split(".")[0] + "_pinyin." + f.split(".")[1])
        rawtable_pinyin = getData3(arg,arg2,pinyindict)
        rawtablelist_pinyin.append(rawtable_pinyin)
        dict_pattern_name_pinyin[pattern_cnt] = arg2.split("/")[-1].split(".")[0]
    if(optargc == "zhongwen"):
        newfw = fwriter 
        do_fun(querylist,rawtablelist,dict_pattern_name,newfw,querylist)
    elif (optargc == "pinyin"):
        newfw = fwriter 
        do_fun(querylist_pinyin,rawtablelist_pinyin, dict_pattern_name_pinyin,newfw,querylist)
    else:
        newfw1 = fwriter + "_" + "zhongwen" 
        do_fun(querylist,rawtablelist,dict_pattern_name,newfw1,querylist)
        newfw2 = fwriter + "_" + "pinyin" 
        do_fun(querylist_pinyin,rawtablelist_pinyin, dict_pattern_name_pinyin,newfw2,querylist)
        combine_file(newfw1,newfw2,fwriter)
    #pm.genNewdomain(domain_name, generate_number_for_each_sentence)
    #print "generate done"
