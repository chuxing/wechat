import os
import sys
import jieba
import codecs


def jiebacut(name):
    fr = codecs.open(name,'r','gb18030',errors='ignore')
    fw = codecs.open(name+"_new",'w','gb18030')
    for rawsentence in fr.readlines():
        newsentence = "".join(rawsentence.split(" "))
        seg_list = jieba.lcut(newsentence)
        sentence = " ".join(seg_list)
        fw.write(sentence)

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        jiebacut(arg)
    #name1 = sys.argv[1]
    #name2 = sys.argv[2]
    #jiebacut(name1)
    #jiebacut(name2)
