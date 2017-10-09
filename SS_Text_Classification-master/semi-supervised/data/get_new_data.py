#######################################################  
#File Name: get_new_data.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-06-30 11:49:24
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    rawunlabeldata = sys.argv[1]
    rawlabeldata = sys.argv[2]
    newunlabeldata = sys.argv[3]
    newdataset = set()
    fw = codecs.open(rawlabeldata,'a','gb18030')
    for root, dirs, files in os.walk(sys.argv[4]):
        for f in files:
            filename = os.path.join(root,f)
            for line in codecs.open(filename, 'r', 'gb18030', errors = 'ignore'):
                newdataset.add(line.strip())
                newline = str(f) + "\t" + str(line)
                print >> fw, newline,
    ufw = codecs.open(newunlabeldata,'w','gb18030')
    unlabelset = set()
    for line in codecs.open(rawunlabeldata,'r','gb18030',errors = 'ignore'):
        line = line.strip()
        if line in unlabelset:
            continue
        elif line in newdataset:
            #print line
            continue
        else:
            unlabelset.add(line)
            print >>  ufw, line
