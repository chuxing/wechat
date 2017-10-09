#######################################################  
#File Name: FileProcess.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-06-29 15:18:30
########################################################  
#!/usr/bin/python  
#-*- coding:utf-8 -*-  
import sys
import codecs
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import time
reload(sys)
sys.setdefaultencoding('utf8')

class FP(object):
    def __init__(self):
        pass

    def write_acc_to_file(self, filename,content):
        fw = codecs.open(filename, 'a','gb18030')
        print >> fw, time.asctime( time.localtime(time.time()))
        print >> fw, "_"*50
        for k,v in content.items():
            print >> fw, k,v
        print >> fw, "-"*50

    def write_file(self, flag, filename,sentence):
        if flag == 0 and os.path.exists(filename):
            #print "*******" + filename
            os.remove(filename)
        #print filename,sentenc
        print >> codecs.open(filename,'a','gb18030'), sentence 

    def read_files(self,rootdir):
        """Read the training and development data from the news tar file.
        The returned object contains various fields that store the data, such as:
        train_data,dev_data: array of documents (array of words)
        train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
        train_labels,dev_labels: the true string label for each document (same length as data)
        The data is also preprocessed for use with scikit-learn, as:
        count_vec: CountVectorizer used to process the data (for reapplication on new data)
        trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
        le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
        target_labels: List of labels (same order as used in le)
        trainy,devy: array of int labels, one for each document
        """
        class Data: pass
        news = Data()
        print "-- train data"
        news.train_data, news.train_fnames, news.train_labels = self.read_tsv(rootdir, "train")
        print len(news.train_data)
        print "-- valid data"
        news.dev_data, news.dev_fnames, news.dev_labels = self.read_tsv(rootdir, "valid")
        print len(news.dev_data)
        #for i in news.train_labels:
            #print repr(i).decode('unicode-escape')
        print "-- transforming data and labels"
        news.count_vect = TfidfVectorizer(analyzer = 'word', norm = 'l2', sublinear_tf = True)  
        news.trainX = news.count_vect.fit_transform(news.train_data)
        news.devX = news.count_vect.transform(news.dev_data)
        news.le = preprocessing.LabelEncoder()
        news.le.fit(news.train_labels)
        news.target_labels = news.le.classes_
        news.trainy = news.le.transform(news.train_labels)
        news.devy = news.le.transform(news.dev_labels)
        return news

    def read_unlabeled(self, filename, news):
        """Reads the unlabeled data.
        The returned object contains three fields that represent the unlabeled data.
        data: documents, represented as sequence of words
        fnames: list of filenames, one for each document
        X: bag of word vector for each document, using the news.vectorizer
        """
        class Data: pass
        unlabeled = Data()
        unlabeled.data = []
        unlabeled.fnames = []
        for index, line in enumerate(codecs.open(filename, 'r', 'gb18030', errors = 'ignore')):
            unlabeled.data.append(line.strip())
            unlabeled.fnames.append(index)
        unlabeled.X = news.count_vect.transform(unlabeled.data)
        return unlabeled

    def read_tsv(self, rootdir, fname):
        tf = codecs.open(rootdir + fname, 'r','gb18030', errors = 'ignore') 
        data = []
        labels = []
        fnames = []
        for linecnt, line in enumerate(tf.readlines()):
            #print repr(line.split("\t")[1].strip()).decode('unicode-escape')
            try:
                data.append(line.split("\t")[1].strip())
                labels.append(str(line.split("\t")[0]))
                fnames.append(linecnt)
            except:
                print fname,linecnt,line
        return data, fnames, labels
