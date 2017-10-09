#!/bin/python
import codecs
from FileProcess import FP
from SemiSC import SemiSC 
import sys

fp = FP()
ssc = SemiSC()

def plot_graphs(x, y, function):
    import matplotlib.pyplot as plt
    plt.plot(x, y, color = 'blue', linewidth = 3)
    plt.axis([0, 6, 0, 20])
    plt.show()

if __name__ == "__main__":
    rootdir = sys.argv[1]
    uldata = sys.argv[2]
    print "Reading data"
    #rootdir = "./data/"
    news = fp.read_files(rootdir)
    print "Training classifier"
    cls_lr = ssc.train_classifier(news.trainX, news.trainy)
    cls_nb = ssc.train_naive_bayes(news.trainX, news.trainy)
    cls_svm = ssc.train_svm(news.trainX, news.trainy)
    
    print "Evaluating"
    #print "LR train_data",
    #ssc.evaluate(news.trainX, news.trainy, cls_lr)
    print "LR valid_data",
    ssc.evaluate(news.devX, news.devy, cls_lr)

    print "------------------------------------------------------------------------------------------"
    #print "NB train_data",
    #ssc.evaluate(news.trainX, news.trainy, cls_nb)
    print "NB valid_data",
    ssc.evaluate(news.devX, news.devy, cls_nb)

    print "------------------------------------------------------------------------------------------"
    #print "SVM train_data",
    #ssc.evaluate(news.trainX, news.trainy, cls_svm)
    print "SVM valid_data",
    ssc.evaluate(news.devX, news.devy, cls_svm)
    ssc.output_acc(rootdir)
    print "Read_unlabeled data"
    unlabeled = fp.read_unlabeled(rootdir + uldata, news)
    print "Semi Supervised"
    #cls_unlabeled, plot_trainX = ssc.addUnlabeled(unlabeled, news.trainX, news.trainy, cls, cls_nb, cls_svm, news)
    ssc.addUnlabeled(rootdir,unlabeled, news.trainX, news.trainy, cls_lr, cls_nb, cls_svm, news)
    # plt.plot(news.trainX, news.trainy, color = 'blue', linewidth = 3)

