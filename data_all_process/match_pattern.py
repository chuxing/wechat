#coding:utf8
import os
import codecs
import sys
import re
reload(sys)
sys.setdefaultencoding('gb2312')

def readfile(rootdir):
    #files = os.listdir(rootdir)
    for file in os.listdir(rootdir):
        path = os.path.join(rootdir,file)
        print path
        if os.path.isdir(path):
            readfile(path)
        else:
            wfilename = os.path.join("videodata/","pattern_" + file)
            print wfilename
            fw = codecs.open(wfilename,'w',encoding='gb18030',errors='ignore')
            #fw2 = codecs.open(wfilename + "_other",'w','gb18030')
            f = codecs.open(path, 'r','gb18030',errors = 'ignore')
            pattern = [line.strip() for line in codecs.open("pattern_video",'r','gb18030').readlines()]
            linecnt = 0
            for rawline in f.readlines():
                linecnt += 1
                if line.startswith("__label__"):
                    line = "".join(rawline.strip().split(" ")[1:])
                else:
                    line =  rawline.strip()
                #flag = 0
                for ipattern in pattern:
                    #print ipattern,line
                    if line.find(ipattern) != -1:
                        flag = 1
                        fw.write(line + "\n")
                        break
                #if flag == 0:
                    #fw2.write(rawline)
            #break
        #print linecnt                
if __name__ == '__main__':
    rootdir = sys.argv[1]
    readfile(rootdir)
