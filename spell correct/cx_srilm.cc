////////////////////////////////////////////////////////
//File Name: cx_srilm.cc
//Author: Chu Xing
//Mail: v_xingzhu@tencent.com  
//Created Time: 2017-07-24 15:02:53
////////////////////////////////////////////////////////
#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include "cx_srilm.h" 
#include "Ngram.h"
#include "Vocab.h"
#include "File.h"
#include <wchar.h>
#include <cmath>
using namespace std;

void cx_srilm::set_srilm(int n_gram, char* lmfilename){
    default_ngram = n_gram;
    vocab = new Vocab;
    ng = new Ngram(*vocab,n_gram);
    File file(lmfilename,"r");
    //ng->debugme(2);
    if(!ng->read(file)){
        cerr << "format error in lm file " << lmfilename << endl;
        exit(1);
    }
}

int cx_srilm::word_id(const char *w){
   return vocab->getIndex(w);
}
double cx_srilm::ngram_logprob(unsigned int w[],int n){
    VocabIndex context[n];
    for(int i = 0 ;i < n - 1;i++){
        context[i] = w[n-i-2];
    }
    context[n-1] = Vocab_None;
    if(LogPtoProb(ng->wordProb(w[n-1],context)) == 0){
        return 0;
    }
    else{
        return -log(LogPtoProb(ng->wordProb(w[n-1],context)));
    }
    //return -lm->wordProb(w[n-1],context);
}

double cx_srilm::get_ngram_score(string sentence,int n){
    char* line = (char*)sentence.c_str();
    VocabString prefix[maxWordsPerLine + 1];
    unsigned numWords = vocab->parseWords(line,prefix,maxWordsPerLine);
    prefix[numWords] = 0;
    unsigned int w[n];
    int tmpid = 0;
    //cout << line<<endl;
    for(unsigned int i = numWords - n; i < numWords; i++){
        //cout<<prefix[i] << " " << word_id(prefix[i])<< " "<<endl;;
        if(word_id(prefix[i]) == -1){
            w[tmpid++] = word_id("<unk>"); 
        }
        else {
            w[tmpid++] = word_id(prefix[i]);
        }
    }
    return cx_srilm::ngram_logprob(w,n);
}

void cx_srilm::sentenceStats(string  sentence, TextStats &stats) {
    double ans;
    VocabString words[maxWordsPerLine + 1];
    unsigned indices[2];
    unsigned numparsed;
    char* scp = (char*)sentence.c_str();
    numparsed = Vocab::parseWords(scp, words, maxWordsPerLine + 1);
    ng->sentenceProb(words, stats);
}


double cx_srilm::getSentenceProb(string sentence) {
    TextStats stats;
    double ans;
    sentenceStats(sentence, stats);
    if(stats.prob == LogP_Zero) ans = BIGEN;
    else ans = -log(LogPtoProb(stats.prob));
    return ans;
}


double cx_srilm::getSentencePpl(string sentence) {
    double ans;
    TextStats stats;
    sentenceStats(sentence,stats);
    int denom = stats.numWords - stats.numOOVs - stats.zeroProbs + stats.numSentences;
    if(denom > 0){
        ans = LogPtoPPL(stats.prob / denom);
    }
    else{
        ans = BIGEN;
    }
    return ans;
}

