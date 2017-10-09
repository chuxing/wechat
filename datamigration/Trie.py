 # -*- coding:utf8 -*- 

class Trie(object):
    def __init__(self):
        self.root = dict()
        self.END = '\0'

    def insert(self, string):
        if string == '\0':return
        index, node,return_index, return_flag = self.findLastNode(string)
        # print index,node
        for char in string[index:]:
            node=node.setdefault(char,{})
        node[self.END] = None

    def find(self, string):
        index, node,return_index,return_flag = self.findLastNode(string)
        # print index,self.END,self.END in node
        # if self.END in node:
        	# print index,repr(node).decode('unicode-escape')
        # index == len(string) and
        return return_flag,return_index 

    def findLastNode(self, string):
    	# print string
    	node = self.root
        index = 0
        return_flag = False 
        return_index = -1
        while index < len(string):
            char = string[index]
            if char == ' ':
                index += 1
                return_index = index 
                continue 
            if char != '' and (char in node):
                node = node[char]
                if self.END in node :
                    return_flag = True 
                    return_index = index + 1
            else:
                break
            index += 1
        return (index, node,return_index,return_flag)
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
