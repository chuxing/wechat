#coding:utf8
from liblinearutil import *
import csv
import jieba
# jieba.load_userdict('wordDict.txt')
import numpy as np
import jieba.posseg as pseg

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
import codecs
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score
import re



from sklearn.grid_search import GridSearchCV
def fenci(contentlist):
	# liststr = ""
	listseg = []
	for sentence in contentlist:
		liststr = ' '.join([sentence[i:i+3] for i in range(0, len(sentence), 3)])
		# print liststr
		listseg.append(liststr)
	return listseg

def readfile(file):
	print file
	src = []
	contentlist = []
	opinionlist = []
	f = codecs.open(file,"rb","gb18030",errors = 'ignore')
	for line in f.readlines():
		linesplit = line.split(" ")
		contentlist.append(linesplit[1])
		opinionlist.append(linesplit[0])
	contentlist = fenci(contentlist)
	src = [contentlist,opinionlist]
	return src
if __name__ == '__main__':
	trainfile = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_raw_data_balance.txt_0.9"
	testfile = "D:/cygwin/home/v_xingzhu/fasttext/reminder/xing_raw_data_balance.txt_0.1"
	train = readfile(trainfile)
	test = readfile(testfile)

	text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(C=1, kernel = 'linear'))])
	text_clf = text_clf.fit(train[0], train[1])
	predicted = text_clf.predict(test[0])
	# print predicted
	print 'SVC',np.mean(predicted == test[1])
	print 'f1 socre weighted',f1_score(predicted, test[1], average='weighted')  
	# print ((predicted == test[1]))
	print set(predicted)
	print metrics.confusion_matrix(test[1],predicted) # 混淆矩阵

	# parameters = {'vect__max_df': (0.4, 0.5, 0.6, 0.7),'vect__max_features': (None, 5000, 10000, 15000),
 #              'tfidf__use_idf': (True, False)}
	# grid_search = GridSearchCV(text_clf, parameters, n_jobs=1, verbose=1)
	# grid_search.fit(content, opinion)
	# best_parameters = dict()
	# best_parameters = grid_search.best_estimator_.get_params()
	# for param_name in sorted(parameters.keys()):
	#     print("\t%s: %r" % (param_name, best_parameters[param_name]))

	# print len(test[0])
	# print len(test[1])
	# for i in test[0]:
	# 	print i[:-1]

		# vectorizer=CountVectorizer()
	# tfidftransformer=TfidfTransformer()
	# tfidf = tfidftransformer.fit_transform(vectorizer.fit_transform(train[0]))
	# print tfidf.shape
 # 	word = vectorizer.get_feature_names()
	# weight = tfidf.toarray()
	# clf = MultinomialNB().fit(tfidf, train[1])
	# docs = ["每天起床。"]
	# new_tfidf = tfidftransformer.transform(vectorizer.transform(docs))
	# predicted = clf.predict(new_tfidf)
	# print predicted
