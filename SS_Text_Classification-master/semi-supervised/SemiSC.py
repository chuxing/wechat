#!/bin/python
from FileProcess import FP
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.calibration import CalibratedClassifierCV
fp = FP()
class SemiSC(object):
    def __init__(self):
        pass

    def train_classifier(self,X, y):
        """Train a classifier using the given training data.
        Trains a logistic regression on the input data with default parameters.
        """
        cls = LogisticRegression(penalty = 'l2', C = 10, tol=0.01)
        cls.fit(X, y)
        self.lrcls = cls
        return cls

    def train_naive_bayes(self,X, y):
        cls = MultinomialNB(alpha = 0.01)
        cls.fit(X,y)
        self.nbcls = cls
        return cls

    def train_svm(self,X, y):
        svm = LinearSVC()
        cls = CalibratedClassifierCV(svm, method = 'isotonic')
        cls.fit(X,y)
        self.svmcls = cls
        return cls

    def evaluate(self,X, yt, cls):
        """Evaluated a classifier on the given labeled data using accuracy."""
        from sklearn import metrics
        yp = cls.predict(X)
        acc = metrics.accuracy_score(yt, yp)
        print "  Accuracy", acc
        if cls == self.lrcls:
            self.lracc = acc
        elif cls == self.nbcls:
            self.nbacc = acc 
        elif cls == self.svmcls:
            self.svmacc = acc
    
    def output_acc(self, rootdir):
        res = {}
        res["lr: "] = self.lracc
        res["nb: "] = self.nbacc
        res["svm: "] = self.svmacc
        fp.write_acc_to_file(rootdir + "res_acc", res)


    def addUnlabeled(self,rootdir,unlabeled, X, y, cls_lr, cls_nb, cls_svm, video):
        yp_lr = cls_lr.predict(unlabeled.X)
        yp_nb = cls_nb.predict(unlabeled.X)
        yp_svm = cls_svm.predict(unlabeled.X)
        pr_proba_lr = cls_lr.predict_proba(unlabeled.X)
        pr_proba_nb = cls_nb.predict_proba(unlabeled.X)
        pr_proba_svm = cls_svm.predict_proba(unlabeled.X)
        labels_lr = video.le.inverse_transform(yp_lr)
        labels_nb = video.le.inverse_transform(yp_nb)
        labels_svm = video.le.inverse_transform(yp_svm)
        train_data, train_fnames, train_labels = video.train_data, video.train_fnames, video.train_labels 
        flag_write = {}
        flag_write["lr__label__video_normal"] = 0
        flag_write["lr__label__video_dianbo"] = 0
        flag_write["lr__label__video_other"] = 0
        flag_write["nb__label__video_normal"] = 0
        flag_write["nb__label__video_dianbo"] = 0
        flag_write["nb__label__video_other"] = 0
        flag_write["svm__label__video_normal"] = 0
        flag_write["svm__label__video_dianbo"] = 0
        flag_write["svm__label__video_other"] = 0
        flag_write["same__label__video_normal"] = 0
        flag_write["same__label__video_dianbo"] = 0
        flag_write["same__label__video_other"] = 0
        for i in xrange(len(unlabeled.fnames)):
            fname = unlabeled.fnames[i]
            maxVal_lr = max(pr_proba_lr[i])
            maxIndex_lr = pr_proba_lr[i].tolist().index(max(pr_proba_lr[i]))
            maxVal_nb = max(pr_proba_nb[i])
            maxIndex_nb = pr_proba_nb[i].tolist().index(max(pr_proba_nb[i]))
            maxVal_svm = max(pr_proba_svm[i])
            maxIndex_svm = pr_proba_svm[i].tolist().index(max(pr_proba_svm[i]))
            #print i,repr(unlabeled.data[i]).decode("unicode-escape")
            fp.write_file(flag_write["lr" + labels_lr[i]],rootdir + "lr/" + labels_lr[i], unlabeled.data[i])
            fp.write_file(flag_write["nb" + labels_nb[i]],rootdir + "nb/" + labels_nb[i], unlabeled.data[i])
            fp.write_file(flag_write["svm" + labels_svm[i]],rootdir + "svm/" + labels_svm[i], unlabeled.data[i])
            #if (labels_lr[i] == labels_nb[i] == labels_svm[i]) and (maxVal_lr > self.lracc) and (maxVal_nb > self.nbacc) and (maxVal_svm > self.svmacc):
            if (labels_lr[i] == labels_nb[i] == labels_svm[i]): 
                if (labels_lr[i] == "__label__video_dianbo" and maxVal_lr > 0.73 and maxVal_nb > 0.73 and maxVal_svm > 0.73) or (labels_lr[i] == "__label__video_normal" and maxIndex_lr > 0.6 and maxVal_nb > 0.6 and maxVal_svm > 0.6) or (labels_lr[i] == "__label__video_other" and maxIndex_lr > 0.99 and maxIndex_nb > 0.99 and maxIndex_svm > 0.99):
                    fp.write_file(flag_write["same" + labels_svm[i]],rootdir + "same/" + labels_svm[i], unlabeled.data[i])
                    flag_write["same" + labels_lr[i]] = 1
            flag_write["lr" + labels_lr[i]] = 1
            flag_write["nb" + labels_nb[i]] = 1
            flag_write["svm" + labels_svm[i]] = 1
