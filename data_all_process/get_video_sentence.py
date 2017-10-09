#!/usr/bin/python  
#-*- coding:utf-8 -*-  
#######################################################  
#File Name: get_video_sentence.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-08-15 16:28:58
########################################################  
from __future__ import unicode_literals
import sys
import codecs
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf8')
jieba.load_userdict("video.dict")
jieba.load_userdict("actor.dict")

__author__ = 'Seven Chu'

def fun(rootdir,outdir,actor_set,video_set):
    for file in os.listdir(rootdir):
        path = os.path.join(rootdir,file)
        print path 
        if os.path.isdir(path):
            fun(path,outdir,actor_set,video_set)
        else:
            wfilename = os.path.join(outdir,"pattern_" + file)
            fw = codecs.open(wfilename,'w',encoding = 'gb18030',errors = 'ignore')
            f = codecs.open(path,'r','gb18030',errors='ignore')
            sentenceset = set()
            for lineid, rawline in enumerate(f.readlines()):
                if lineid % 100000 == 0:
                    print lineid,rawline,
                flag = 0
                if rawline.startswith("__label__"):
                    line = "".join(rawline.strip().split(" ")[1:])
                else:
                    line = rawline.strip()
                linelist = jieba.lcut(line) 
                for index in range(0,len(linelist)):
                    if linelist[index] in actor_set:
                        linelist[index] = "<actor>"
                        flag = 1
                    elif linelist[index] in video_set:
                        linelist[index] = "<video>"
                        flag = 1
                if flag == 1:
                    newsentence = "".join(linelist)
                    sentenceset.add(newsentence + "\n")
            for i in sentenceset:
                fw.write(i)

            
if __name__ == '__main__':
    fractorname = sys.argv[1]
    frvideoname = sys.argv[2]
    rootdir = sys.argv[3]
    outdir = sys.argv[4]
    fractor = codecs.open(fractorname,'r','utf8')
    frvideo = codecs.open(frvideoname,'r','utf8')
    actor_set = set()
    video_set = set()
    for line in fractor.readlines():
        actor_set.add(line.strip()) 
    for line in frvideo.readlines():
        video_set.add(line.strip())
    #for i in video_set:
        #print i
    fun(rootdir,outdir,actor_set,video_set)


