////////////////////////////////////////////////////////
//File Name: cx_test_for_srilm.cc
//Author: Chu Xing
//Mail: v_xingzhu@tencent.com  
//Created Time: 2017-07-24 17:33:56
////////////////////////////////////////////////////////
#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <wchar.h>
#include "cx_srilm.h"
#include "cx_Trie.h"
using namespace std;
int main(int argc, char *argv[]){
    char* lmfilename = argv[1];
    string testsentence = "我";
    string testsentence2 = "播" ;
    cx_srilm mysrilm;
    mysrilm.set_srilm(3,lmfilename);
    cout << mysrilm.get_ngram_score(testsentence,1)<<endl;
    cout << mysrilm.get_ngram_score(testsentence2,1)<<endl;
    cout << mysrilm.getSentenceProb(testsentence)<<endl;
    cout << mysrilm.getSentenceProb(testsentence2)<<endl;
    cout << mysrilm.getSentencePpl(testsentence)<<endl;
    cout << mysrilm.getSentencePpl(testsentence2)<<endl;
    cx_Trie mytrie;
    mytrie.insert("hello");
    mytrie.insert("high");
    mytrie.insert("法蜗牛的");
    mytrie.insert("你好得名的阿");
    //vector<string>gen_word = mytrie.find("hel");
    //for(unsigned int i = 0 ; i < gen_word.size();i++){
        //cout<<gen_word[i]<<"  ";
    //}
    //cout<<endl;

    //mytrie.print_all();
    return 0;
}

