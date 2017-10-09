/*
 * testNgram --
 *	Rudimentary test for Ngram LM class
 */

#ifndef lint
static char Copyright[] = "Copyright (c) 2005, SRI International.  All Rights Reserved.";
static char RcsId[] = "@(#)$Header: /home/srilm/CVS/srilm/lm/src/testNgram.cc,v 1.2 2016/06/24 00:18:40 stolcke Exp $";
#endif

#include <stdio.h>

#include "Ngram.h"
#include "Vocab.h"
#include "File.h"
#include <iconv.h> 
#include <typeinfo>
using namespace std;
static Vocab *vocab;
static Ngram *lm;

static void trigram_init(char *filename) {
    vocab = new Vocab;
    assert(vocab != 0);

    lm = new Ngram(*vocab, 3);
    assert(lm != 0);

    File file(filename, "r");

    lm->debugme(1);

    if (!lm->read(file)) {
	cerr << "format error in lm file " << filename << endl;
	exit(1);
    }
}

static int word_id(const char *w) {
    return vocab->getIndex(w);
}

static double trigram_logprob(unsigned w1, unsigned w2, unsigned w3) {
    VocabIndex context[3];

    context[0] = w2;
    context[1] = w1;
    context[2] = Vocab_None;

    return lm->wordProb(w3, context);
}

static double trigram_prob(unsigned w1, unsigned w2, unsigned w3) {

    //return (trigram_logprob(w1, w2, w3));
    //return LogPtoProb(trigram_logprob(w1, w2, w3));
    return -log(LogPtoProb(trigram_logprob(w1, w2, w3)));
}



int main (int argc, char *argv[])
{
    char* lmfilename = argv[1];
    char* textfilename = argv[2];

    trigram_init(lmfilename);

    int w0 = word_id("<s>");
    int w2 = word_id("</s>");
    int unkid  = word_id("<unk>");

    std::cout << w0 << " " << w2 << " " << unkid << endl;

    // start reading a query
	File inFile(textfilename, "r");
	File outFile(stdout);

	VocabString prefix[maxWordsPerLine+1];
    string tmpstr = "ÎÒ Ïë ¿´";
    char* line = (char*)tmpstr.c_str();
    cout<< line << endl;
    unsigned numWords = vocab->parseWords(line,prefix,maxWordsPerLine);
    prefix[numWords] = 0;
    std::cout << numWords << endl;
    for (int i = 0; i < numWords; i++) {
        cout << prefix[i]<<" ";
        cout<<endl;
        std::cout << word_id(prefix[i]) << " ";
    }
    double score = trigram_prob(word_id(prefix[0]),word_id(prefix[1]),word_id(prefix[2]));
    cout<<"score: "<<score<<endl;
    //char *line;
    //while ((line = inFile.getline())) {
        //cout<<line<<endl;
        //unsigned numWords = vocab->parseWords(line, prefix, maxWordsPerLine);
        //prefix[numWords] = 0;

            //std::cout << numWords << endl;
            //for (int i = 0; i < numWords; i++) {
                //cout<<prefix[i]<<" ";
                //cout<<endl;
                //std::cout << word_id(prefix[i]) << " ";
            //}
            //std::cout << endl;
    //}

    exit(0);
}
