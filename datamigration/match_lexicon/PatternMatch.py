# -*- coding:utf8 -*- 

from Trie import Trie
import codecs
class PatternMatch(object):
    """docstring for PatternMatch"""
    def __init__(self, querylist, rawtable, dict_pattern_name):
        super(PatternMatch, self).__init__()
        self.querlist = querylist
        self.rawtable = rawtable
        self.dict_pattern_name = dict_pattern_name

    def rawtableProcess(self):
        self.rawtrie = []
        for table in self.rawtable:
            # if len(table) == 0 or table == '\n':continue
            tree = Trie()
            for words in table:
                # if tableid == 0 :print words
                if len(words.strip("\r\n")) == 0 or words == '\0':continue
                tree.insert(words.strip())
            self.rawtrie.append(tree)
            del tree

    def matchQuery(self):
        self.output = []
        for query in self.querlist:
            querycnt = 0
            #print repr(query).decode('unicode-escape'),
            allnewsentence = []
            for sentence in query:
                sentence = sentence.strip(" ").strip("\r\n")
                dict_index_id = {}
                dict_index_id[0] = 0
                dict_id_index = {}
                dict_id_index[0] = 0
                cmpid = 1
                #print sentence.encode('utf8')
                for tmpindex in range(0,len(sentence)):
                    if sentence[tmpindex] == ' ':
                        dict_index_id[tmpindex + 1] = cmpid
                        dict_id_index[cmpid] = tmpindex + 1
                        cmpid += 1
                dict_index_id[len(sentence)] = cmpid
                dict_id_index[cmpid] = len(sentence)
                #print dict_index_id,dict_id_index
                self.newsentence = sentence
                if querycnt % 10000 == 0:
                    print "query:" + str(querycnt)
                querycnt += 1
                for treeid in range(len(self.rawtrie)):
                    sindex = 0
                    sid = 0
                    sentenceflag = 0
                    tindex = -1
                    maxlength = 0
                    while sindex < len(sentence):
                        if sentence[sindex] == ' ':
                            sindex += 1
                            continue
                        subsentence = sentence[sindex:]
                        flag,index = self.rawtrie[treeid].find(subsentence)
                        #print flag,index
                        if flag == True and index > maxlength and (sindex + index == len(sentence) or sentence[sindex + index - 1] == ' '):
                            maxlength = index
                            tindex = sindex
                        sindex = dict_id_index[sid + 1]
                        sid += 1
                    if tindex != -1:
                        self.newsentence += ("\t" + self.dict_pattern_name[treeid] + "#" + str(dict_index_id[tindex]) + ":" + str(dict_index_id[tindex + maxlength]))
                allnewsentence.append(self.newsentence)
                #print allnewsentence
            self.output.append(allnewsentence)

    def genOutput(self,outputfile,writequerlist):
        fw = codecs.open(outputfile,'w','gb18030')
        for listindex,sentencelist in enumerate(self.output):
            for sentenceindex,sentence in enumerate(sentencelist):
                sentence = sentence.replace(sentence.split("\t")[0],writequerlist[0][sentenceindex])
                fw.write(sentence + "\n")
