#encoding=utf-8
from zhcnSegment import *
from fileObject import FileObj
from sentenceSimilarity import SentenceSimilarity
from sentence import Sentence
import codecs

if __name__ == '__main__':
    # 读入训练集
    file_obj = FileObj(r"../chat/row_chat.txt")
    train_sentences = file_obj.read_lines(1)
    print "train "
    # 读入测试集1
    file_obj = FileObj(r"../chat/pattern_chat.txt")
    test1_sentences = file_obj.read_lines(2)

    # 读入测试集2
    # file_obj = FileObj(r"testSet/testSet2.txt")
    # test2_sentences = file_obj.read_lines()

    # 分词工具，基于jieba分词，我自己加了一次封装，主要是去除停用词
    seg = Seg()

    # 训练模型
    ss = SentenceSimilarity(seg)
    ss.set_sentences(train_sentences)
    print "train done"

    # ss.TfidfModel()         # tfidf模型
    ss.LsiModel()         # lsi模型
    # ss.LdaModel()         # lda模型
    print "model done"

    # 测试集1
    right_count = 0
    fw = codecs.open("extend_chat.txt", 'a', 'gb2312', errors = 'ignore')
    for i in range(0,len(train_sentences)):
        for j in range(len(test1_sentences)):
            sentencelist = ss.similarity(test1_sentences[j])
            for sentence in sentencelist:
			    fw.write(sentence)
            #print train_sentences[i],test1_sentences[j], str(sentence.score)
        # if i != sentence.id:
        #     print str(i) + " wrong! score: " + str(sentence.score)
        # else:
        #     right_count += 1
        #     print str(i) + " right! score: " + str(sentence.score)

    #print "正确率为: " + str(float(right_count)/len(train_sentences))
