 # -*- coding:utf8 -*- 
import os
import marisa_trie
import codecs
import random
import linecache  
def write2file(flag,fileid,method,string):
    
    # print fileid,type(string)
    filename = "E:\\code\\datamigration\\newdomain\\newdomain_" +  method + fileid + ".txt"
    if flag == 1 and os.path.exists(filename):os.remove(filename)
    f = codecs.open(filename,'a','gb2312')
    f.write(string.decode('utf8') + "\n")
def readfromfile(fileid,linecnt):
    filename = "E:\\code\\datamigration\\newtable\\newtable" +  fileid + ".txt"
    f = codecs.open(filename,'r','gb2312')
    tmpstr = ""
    # print linecnt,randomline
    # print filename
    try:
        randomline = random.randrange(1,linecnt)
        tmpstr =  (linecache.getline(filename,randomline).decode('gb2312').encode('utf8')).rstrip("\n")
        # tmpstr = 
    except Exception as e:
        pass
        # print "read error"
    # print tmpstr+"sdf"
    return tmpstr

class Trie:
    def __init__(self):
        self.root = dict()
        self.END = '%'
    def insert(self, string):
        #注意插入空行的问题-----待处理
        # print string
        index, node = self.findLastNode(string)

        # print index,node
        for char in string[index:]:
            node=node.setdefault(char,{})
        node[self.END] = None

    def find(self, string):
        # print string
        index, node = self.findLastNode(string)
        # print index,self.END,self.END in node
        # if self.END in node:
            # print index,repr(node).decode('unicode-escape')
        # index == len(string) and
        return self.END in node,index
    def findLastNode(self, string):
        # print string
        node = self.root
        index = 0
        while index < len(string):
            char = string[index]
            if char != '' and (char in node):
                node = node[char]
            else:
                break
            index += 1
        return (index, node)
    def printTree(self, node, layer):
        if node == None:
            return '\n'
        res = []
        items = sorted(node.items(), key=lambda x:x[0])
        res.append(items[0][0])
        res.append(self.printTree(items[0][1], layer+1))
        for item in items[1:]:
            res.append('.' * layer)
            res.append(item[0])
            res.append(self.printTree(item[1], layer+1))
        return ''.join(res)
    def __str__(self):
        # print "asdfasdfasdf"
        # print self.printTree(self.root, 0).encode('gb2312')
        return unicode(self.printTree(self.root, 0)).encode('utf-8')

class PatternMatch(object):
    """docstring for PatternMatch"""
    def __init__(self, querylist, rawtable, newtable):
        super(PatternMatch, self).__init__()
        self.querlist = querylist
        self.rawtable = rawtable
        self.newtable = newtable
    def rawtableProcess(self):
        self.rawtrie = []
        for table in self.rawtable:
            if len(table) == 0 or table == '\n':continue
            tree = Trie()
            for words in table:
                tree.insert(words.strip("\r\n"))
            self.rawtrie.append(tree)
            del tree
        # print self.rawtrie[3]
    def matchQuery(self):
        self.newdomain = []
        queryid = 0
        for query in self.querlist:
            print queryid
            queryid += 1
            querycnt = 0
            # print repr(query).decode('unicode-escape'),
            allnewsentence = []
            for sentence in query:
                # print querycnt
                querycnt += 1
                sindex = 0
                newsentence = []
                sentence = sentence.rstrip("\r\n")
                sentenceflag = 0
                while sindex < len(sentence):
                    subsentence = sentence[sindex:]
                    # print subsentence[:-1],
                    # print subsentence
                    id = -1
                    maxlength = 0
                    for treeid in range(len(self.rawtrie)):
                        # print self.rawtrie[treeid]
                        flag,index = self.rawtrie[treeid].find(subsentence)
                        if flag == True and index > maxlength:
                            maxlength = index
                            id = treeid
                    if id == -1:
                        newsentence.append(subsentence[0])
                        sindex += 1
                    else:
                        sentenceflag = 1
                        newsentence.append("[["+str(id)+"]]")
                        sindex += max(1,maxlength)
                    # print subsentence,flag,index,maxlength,repr(newsentence).decode('unicode-escape')
                if sentenceflag:
                    allnewsentence.append(newsentence)
                else:
                    allnewsentence.append("!@#$%^&*()_+")
                # print repr(allnewsentence).decode('unicode-escape')
            self.newdomain.append(allnewsentence)
    def genNewdomain(self,cnt):
        # print "********"
        for domainid in range(len(self.newdomain)):
            print domainid
            deleteflag = 0
            # print "&&&&&&&&&&&&&"
            for sentence in self.newdomain[domainid]:
                deleteflag += 1
                if sentence == "!@#$%^&*()_+":
                    write2file(deleteflag, str(domainid+1), "trie", sentence)
                    continue
                nowcnt = 0
                # print repr(sentence).decode('unicode-escape')
                while nowcnt < cnt:    
                    nowcnt += 1
                    newsentence =""
                    pattern = ""
                    for word in sentence:
                        pattern += word.encode('utf8')
                        # print word
                        if word.startswith("[["):
                            # print "*******" + word
                            fileid = word[2]
                            # print int(fileid)+1
                            newtableword = readfromfile(str(int(fileid)),len(self.newtable[int(fileid)]))
                            # print (newtableword)
                            # print type(newtableword)
                        else:
                            # print type(word)
                            newtableword = word.encode('utf8')
                            # print type(newtableword)
                        # print newtableword
                        newsentence += newtableword
                    # print newsentence
                    write2file(deleteflag, str(domainid+1), "trie", newsentence)
                    deleteflag += 1
                # print repr(sentence).decode('unicode-escape')

class GrammarAnalysis(object):
    """docstring for GrammarAnalysis"""
    def __init__(self, querylist, rawtable, newtable):
        super(GrammarAnalysis, self).__init__()
        self.querlist = querylist
        self.rawtable = rawtable
        self.newtable = newtable
    
def getQuery(rootdir):
    querylist = []
    for file in os.listdir(rootdir):
        query = []
        path = os.path.join(rootdir,file)
        f = codecs.open(path,"r",'gb2312',errors='ignore')
        # print path
        # if path.endswith("1.txt"):continue
        for line in f.readlines():
            # print line
            query.append(line.strip("\r\n"))
        querylist.append(query)
    return querylist
def getRawtable(rootdir):
    rawtable = []
    for file in os.listdir(rootdir):
        table = []
        path = os.path.join(rootdir,file)
        # print path
        f = codecs.open(path,"r",'gb2312',errors='ignore')
        for line in f.readlines():
            table.append(line.strip("\r\n"))
        rawtable.append(table)
    return rawtable
def getNewtable(rootdir):
    newtable = []
    for file in os.listdir(rootdir):
        table = []
        path = os.path.join(rootdir,file)
        # print path
        f = codecs.open(path,"r",'gb2312')
        for line in f.readlines():
            table.append(line.strip("\r\n"))
        newtable.append(table)
    return newtable
        
if __name__ == '__main__':
    prestring = "E:\code\datamigration"
    querylist = getQuery(prestring + "\\query\\")
    rawtable = getRawtable(prestring + "\\rawtable\\")
    newtable = getNewtable(prestring + "\\newtable\\")
    # for i in rawtable:
    #     for j in i :
    #         print j
    # print "read done"
    # pm = PatternMatch(querylist, rawtable, newtable)
    # print "init done"
    # pm.rawtableProcess()
    # print "trie done"
    # pm.matchQuery()
    # print "mathch done"
    # pm.genNewdomain(1)
    # print "generate done"
    # ga = GrammarAnalysis(querylist, rawtable, newtable)
