#encoding=utf-8
import codecs

class FileObj(object):

    def __init__(self,filepath):
        self.filepath = filepath

    # 按行读入数据，返回一个List
    def read_lines(self,flag):
        self.sentences = []
        cnt = 0
        file_obj = codecs.open(self.filepath,'r','gb2312')
        while True:
            cnt += 1
            if flag == 1 and cnt == 1000:break
            line = file_obj.readline()
            line=line.strip('\r\n')
            if not line:
                break
            self.sentences.append(line)
        file_obj.close()

        return self.sentences
