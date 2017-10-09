////////////////////////////////////////////////////////
//File Name: cx_Trie.cc
//Author: Chu Xing
//Mail: v_xingzhu@tencent.com  
//Created Time: 2017-07-26 16:21:36
////////////////////////////////////////////////////////
#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include "cx_Trie.h"
#include "Encoder/Text.h"
#include "Encoder/GbkText.h"
#include "Encoder/UtfText.h"
using namespace std;

vector<string>cx_Trie::gettokens(string sentence){
    GbkText gbk(sentence);
    vector<string>tokens(gbk.tokenize());
    return tokens;
}


int cx_Trie::canbeinsert(string tmpstr,string need_insert){
    pair<mmit,mmit>pos = trienode.equal_range(tmpstr);
    int flag = 1;
    while(pos.first != pos.second){
        if(pos.first++->second == need_insert){
            flag = 0;
            break;
        }
    }
    return flag;
}

void cx_Trie::insert(string sentence){
    //cout<<sentence<<endl;
    vector<string>tokens = gettokens(sentence);
    for(unsigned int i = 0 ; i < tokens.size();i++){
        //cout<<tokens[i]<<" ";
        string tmpstr = "";
        string tmpstr_pos = "";
        tmpstr += tokens[i];
        string need_insert = "";
        if(i != tokens.size()-1)
            need_insert = tmpstr_pos + tokens[i+1];
        else 
            need_insert = is_end;
        //cout<<tmpstr <<" "<<need_insert<<endl;
        int flag = canbeinsert(tmpstr,need_insert);
        if(flag){
            trienode.insert(pair<string,string>(tmpstr,need_insert));
        }
    }
}

void cx_Trie::insert_prefix(string sentence){
    vector<string>tokens = gettokens(sentence);
    string nowstr = "";
    for(unsigned int i = 0; i < tokens.size();i++){
        string tmpstr_pos = "";
        nowstr += tokens[i];
        string need_insert = "";
        if(i != tokens.size()-1)
            need_insert = tmpstr_pos + tokens[i + 1];
        else 
            need_insert = is_end;
        int flag = canbeinsert(nowstr,need_insert);
        if(flag)
            trienode.insert(pair<string,string>(nowstr,need_insert));
    }
}

void cx_Trie::insert_suffix(string sentence){
    vector<string>tokens = gettokens(sentence);
    string nowstr = ""; 
    for(int i = tokens.size() - 1; i >= 0;i--){
        string tmpstr_pre = "";
        nowstr = tokens[i] + nowstr;
        string need_insert = "";
        if(i != 0)
            need_insert = tmpstr_pre + tokens[i-1];
        else 
            need_insert = is_end;
        int flag = canbeinsert(nowstr,need_insert);
        if(flag)
            trienode.insert(pair<string,string>(nowstr,need_insert));
    }
}

void cx_Trie::insert_name(string sentence){
    vector<string>tokens = gettokens(sentence);
    if(tokens.size() < 2){
        return;
    }
    string xing = tokens[0];
    string ming = "";
    for(unsigned int i = 1; i < tokens.size();i++){
       ming +=  tokens[i];
    }
    trienode.insert(pair<string,string>(xing,ming));
}

set<string>cx_Trie::find(string sentence,int flag){
    set<string>word_find;
    string pattern = sentence;
    if(sentence.size() == 0) return word_find;
    //GbkText gbk(sentence);
    //vector<string>tokens(gbk.tokenize());
    //if(tokens.size() == 0) return word_find;
    //string pattern = tokens[tokens.size()-1];
    //cout<<"insert prefix: "<<pattern<<endl;
    //string pattern = sentence.substr(sentence.length()-1);
    mmit beg = trienode.lower_bound(pattern);
    mmit end = trienode.upper_bound(pattern);
    while(beg != end){
        if(beg->second == is_end and flag == 0) {
            beg++;
            continue;
        }
        //cout<<"insert find: "<<beg->second<<endl;
        word_find.insert(beg->second);
        beg++;
    }
    return word_find;
}

set<string>cx_Trie::find_prefix(string sentence){
    vector<string>tokens = gettokens(sentence);
    string nowstr = "";
    set<string>word_find;
    for(int i = tokens.size() -1 ;i >= 0;i--){
        nowstr = tokens[i] + nowstr;
        set<string>tmpfind = find(nowstr);
        word_find.insert(tmpfind.begin(),tmpfind.end());
    }
    return word_find;
}

set<string>cx_Trie::find_suffix(string sentence){
    vector<string>tokens = gettokens(sentence);
    string nowstr = "";
    set<string>word_find;
    for(unsigned int i = 0; i < tokens.size();i++){
        nowstr += tokens[i];
        set<string>tmpfind = find(nowstr);
        word_find.insert(tmpfind.begin(),tmpfind.end());
    }
    return word_find;
}

int cx_Trie::find_skip_length(string sentence,vector<string>subfix){
    //cout << sentence<<endl;
    vector<string>tokens = gettokens(sentence);
    string xing = tokens[0];
    set<string>ming = find(xing);
    int index = 0;
    for(int i = int(subfix.size()-1);i >= 0;i--){
        string tmpstr = subfix[i];
        //cout<<tmpstr<<endl;
        if(ming.find(tmpstr) != ming.end()){
           index = gettokens(tmpstr).size() + 1; 
           break;
        }
    }
    //int index = 0;
    //string tmpstr = "";
    //for(unsigned int i = 1; i < tokens.size();i++){
        //tmpstr += tokens[i];
        //if(ming.find(tmpstr) != ming.end()){
            //index = int (i) + 1;
            ////break;
        //}
    //}
    return index;
}

void cx_Trie::print_all(){
    for(firstit = trienode.begin();firstit != trienode.end();){
        cout<<firstit->first<<"=>";
        pair<mmit,mmit>res = trienode.equal_range(firstit->first);
        for(firstit = res.first; firstit != res.second;firstit++){
            cout << firstit->second << " ";
        }
        cout<<endl;
    }
}

void cx_Trie::print_one(string word){
    mmit beg = trienode.lower_bound(word);
    mmit end = trienode.upper_bound(word);
    while(beg != end){
        cout<<beg->second<<"  ";
        beg++;
    }
    cout<<endl;
}

int cx_Trie::get_pos_num(string word){
    return trienode.count(word);
}
