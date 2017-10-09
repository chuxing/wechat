 # -*- coding:utf8 -*- 

from Trie import Trie
import codecs
from FileProcess import FileProcess 
class PatternMatch(object):
    """docstring for PatternMatch"""
    def __init__(self, querylist, rawtable, newtable,querylabellist):
        super(PatternMatch, self).__init__()
        self.querlist = querylist
        self.rawtable = rawtable
        self.newtable = newtable
        self.querylabellist = querylabellist

    def rawtableProcess(self):
        self.rawtrie = []
        for table in self.rawtable:
            tree = Trie()
            for words in table:
                if len(words.strip("\r\n")) == 0 or words == '\0':continue
                tree.insert(words.strip(""))
            self.rawtrie.append(tree)
            del tree

    def matchQuery(self):
        self.newdomain = []
        queryid = 0
        for query in self.querlist:
            print "queryid" + str(queryid)
            queryid += 1
            querycnt = 0
            # print repr(query).decode('unicode-escape'),
            allnewsentence = []
            for sentence in query:
                if querycnt % 10000 == 0: 
                    print querycnt,sentence
                querycnt += 1
                sindex = 0
                newsentence = []
                sentence = sentence.strip("")
                sentenceflag = 0
                while sindex < len(sentence):
                    subsentence = sentence[sindex:]
                    id = -1
                    maxlength = 0
                    for treeid in range(len(self.rawtrie)):
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
                if sentenceflag:
                    allnewsentence.append(newsentence)
                else:
                    allnewsentence.append("!@#$%^&*()_+")
                # print repr(allnewsentence).decode('unicode-escape')
            self.newdomain.append(allnewsentence)

    def genNewdomain(self,domain,cnt):
        fp = FileProcess() 
        for domainid in range(len(self.newdomain)):
            print "domainid: " + str(domainid)
            deleteflag = 0
            for sentenceindex,sentence in enumerate(self.newdomain[domainid]):
                deleteflag += 1
                if sentence == "!@#$%^&*()_+":
                    fp.write2file(domain,deleteflag, str(domainid+1), "trie", sentence)
                    continue
                nowcnt = 0
                # print repr(sentence).decode('unicode-escape')
                while nowcnt < cnt:    
                    nowcnt += 1
                    newsentence = str(self.querylabellist[domainid][sentenceindex] + " ")
                    pattern = ""
                    for word in sentence:
                        pattern += word.encode('utf8')
                        if word.startswith("[["):
                            endid= word.index(']]')
                            fileid = word[2:endid]
                            newtableword = fp.readfromfile(domain,str(int(fileid)),len(self.newtable[int(fileid)]))
                        else:
                            newtableword = word.encode('utf8')
                        newsentence += newtableword
                    fp.write2file(domain,deleteflag, str(domainid+1), "trie", newsentence)
                    deleteflag += 1
                # print repr(sentence).decode('unicode-escape')
