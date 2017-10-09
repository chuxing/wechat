#ifndef SRILM_H
#define SRILM_H
#include <string>
#include <iostream>
#include "Ngram.h"
#include "Vocab.h"
#include "File.h"
#include <wchar.h>
#include "LM.h"
using namespace std; 

class cx_srilm{
    public:
        void set_srilm(int n_gram,char* lmfilename);
        //void ngram_init(char* filename);
        int word_id(const char *w);
        double ngram_logprob(unsigned int w[],int n);
        double get_ngram_score(string sentence,int n);
        void sentenceStats(string sentence,TextStats &stats);
        double getSentenceProb(string sentence);
        double getSentencePpl(string sentence);
    private:
        int default_ngram;
        Ngram *ng;
        Vocab *vocab;
        string sentence;
        const int BIGEN = 99;
};
#endif
