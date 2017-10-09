#ifndef TRIE_H
#define TRIE_H 
#include <string>
#include <map>
#include <iostream>
#include <vector>
#include <set>
using namespace std;
class cx_Trie{
    public:
        vector<string>gettokens(string sentence);
        int canbeinsert(string tmpstr,string need_insert);
        void insert(string sentence);
        void insert_prefix(string sentence);
        void insert_suffix(string sentence);
        void insert_name(string sentence);
        set<string>find_prefix(string sentence);
        set<string>find_suffix(string sentence);
        set<string>find(string sentence,int flag = 0);
        int find_skip_length(string sentence,vector<string>subfix);
        void print_all();
        void print_one(string word);
        int get_pos_num(string word);
    private:
        string is_end = "$END$";
        multimap<string,string>trienode;
        multimap<string,string>::iterator firstit;
        typedef multimap<string,string>::iterator mmit;
        pair<string,string>p;
};
#endif
