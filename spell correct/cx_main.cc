////////////////////////////////////////////////////////
//File Name: cx_main1.cc
//Author: Chu Xing
//Mail: v_xingzhu@tencent.com  
//Created Time: 2017-07-20 14:10:07
////////////////////////////////////////////////////////
#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <vector>
#include <map>
#include <iomanip>
#include <set>
#include <sstream>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <cstring>
#include "cx_Trie.h"
#include "cx_srilm.h"
#include "Encoder/Text.h"
#include "Encoder/GbkText.h"
#include "Encoder/UtfText.h"
#include "set"
using namespace std;
char* inputfilename; //输入文件
char* dictreplacefilename; //替换词典文件
char* songfilename; //插入词典文件
char* outputfilename;//输出文件
char* lmfilename; //模型文件
char* singerfilename; // 歌手文件
map<string,string>word2pinyin;
multimap<string,string>pinyin2word;
vector<vector<string>>sentencesufix;
cx_Trie mytrie;
cx_Trie singertrie;
cx_Trie songtrie;
cx_srilm mysrilm;
int n_gram; //定义n_gram中n的大小 
int change_cnt; //定义每个句子最多可以改变的次数
double insert_score;//定义插入字时的惩罚参数
double delete_score;//定义删除字时的惩罚参数
double replace_score;//定义改变一个字时的惩罚参数
double no_change_score;//定义某个字不变时惩罚参数
int candidate_cnt;//定义每个字最多能产生的候选子句个数
int output_cnt;//定义输出候选子句个数
int not_process_length;
int not_process_score;
set<string>exclude_word{"电视剧","听","播","放","吧","吗","的","唱","了","嘛","啊","歌","是","换","搜"};
//int exclude_insert_word_num;//定义某个字可以进行insert操作的最大可能候选词个数
struct cmp_map{
    bool operator()(const pair<string,double> &p1, const pair<string,double> &p2){
        return p1.second < p2.second;
    }
};
map<pair<string,double>,pair<int,string>,cmp_map>map_now;

void debug_print(string info){
    cout << info<<endl;
}

string int2string(int n){ 
    stringstream stream; 
    string tmpstr;
    stream.str("");
    stream << n;
    stream >> tmpstr;
    //cout <<n <<":"<<tmpstr<<endl;
    return tmpstr;
}

map<char,string>get_replace_char(){
    map<char,string>similarchar;
    similarchar.insert(make_pair('q',"w"));
    similarchar.insert(make_pair('w',"qe"));
    similarchar.insert(make_pair('e',"wr"));
    similarchar.insert(make_pair('r',"et"));
    similarchar.insert(make_pair('t',"ry"));
    similarchar.insert(make_pair('y',"tu"));
    similarchar.insert(make_pair('u',"yi"));
    similarchar.insert(make_pair('i',"uo"));
    similarchar.insert(make_pair('o',"ip"));
    similarchar.insert(make_pair('p',"o"));
    similarchar.insert(make_pair('a',"s"));
    similarchar.insert(make_pair('s',""));
    similarchar.insert(make_pair('d',""));
    similarchar.insert(make_pair('f',""));
    similarchar.insert(make_pair('g',""));
    similarchar.insert(make_pair('h',""));
    similarchar.insert(make_pair('j',""));
    similarchar.insert(make_pair('k',"l"));
    similarchar.insert(make_pair('l',""));
    similarchar.insert(make_pair('z',"x"));
    similarchar.insert(make_pair('x',"zc"));
    similarchar.insert(make_pair('c',"xv"));
    similarchar.insert(make_pair('v',"cb"));
    similarchar.insert(make_pair('b',"vn"));
    similarchar.insert(make_pair('n',"bm"));
    similarchar.insert(make_pair('m',"n"));
    return similarchar;
}

vector<string> chineseoneword(string sentence){
    GbkText gbk(sentence);
    vector<string>tokens(gbk.tokenize());
    return tokens;
}

string convchinese(string line){
    vector<string>tokens = chineseoneword(line);
    string rawsentence = "";
    for(auto val : tokens){
        rawsentence += val;
    }
    return rawsentence;
}

string strip(string tmpstr){
    char *str = (char*)tmpstr.data();
    int i,len;
    len = strlen(str);
    for(i = 0;i < len; i++)
        if(str[i] != ' ') break;
    memmove(str,str+i,len-i+1);
    len = strlen(str);
    for(i = len-1; i >= 0;i--){
        if(str[i] != ' ' and str[i] != '\n' and str[i] != '\r') break;
    }
    str[i+1] = '\0';
    return string(str);
}

vector<string>split(const string& s,const string& c){
    vector<string>v;
    std::string::size_type pos1, pos2;
    pos2 = s.find(c);
    pos1 = 0;
    while(std::string::npos != pos2){
        v.push_back(s.substr(pos1, pos2-pos1));
        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length())
        v.push_back(s.substr(pos1));
    return v;
}


string getngramstring(string sentence){
    string newsentence = "";
    vector<string>tokens = chineseoneword(sentence);
    for(unsigned int i = 0;i < tokens.size();i++){
        newsentence += (" " + tokens[i]);
    }
    newsentence = strip(newsentence);
    return newsentence;
}

double get_lm_score(string sentence,int i){
    vector<string>tokens = chineseoneword(sentence);
    double score = 0.0;
    double score_suff = 0.0;
    string newsentence = getngramstring(sentence);
    //cout << newsentence<<endl;
    if(int(tokens.size() == 1)){
        score = 0.0;
    }
    else if(int(tokens.size()) < n_gram){
        score = mysrilm.get_ngram_score(newsentence,int(tokens.size())); 
    }
    else{
        score = mysrilm.get_ngram_score(newsentence,n_gram);
    }
    if(sentencesufix[i].size() != 0){
        newsentence = newsentence += (" "+ sentencesufix[i][0]);
        if (int(tokens.size() + 1 < n_gram)){
            score_suff = mysrilm.get_ngram_score(newsentence,int(tokens.size()) + 1);
        }
        else{
            score_suff = mysrilm.get_ngram_score(newsentence,n_gram);
        }
    }
    //cout<< "lm score of " << newsentence <<"  score:  "<<score<<endl;
    //return score;
    return score + score_suff;
}

vector<string> get_replace_word_from_pinyin(string rawword){
    vector<string>gen_word;
    string pinyin = "";
    map<string,string>::iterator it = word2pinyin.find(rawword);
    if(it != word2pinyin.end()){
        pinyin = it->second;
    }
    else{
        return gen_word;
    }
    typedef multimap<string,string>::const_iterator mmit;
    mmit beg = pinyin2word.lower_bound(pinyin);
    mmit end = pinyin2word.upper_bound(pinyin);
    while(beg != end){
        if(beg->second != rawword){
            gen_word.push_back(beg->second);
        }
        beg++;
    }
    return  gen_word;
}

void get_new_map(string sentence,double rawscore,int change_num,double pan_score,string preopt,int index,string opt){
    double sen_score = get_lm_score(sentence,index);
    sen_score += (rawscore + pan_score);
    pair<string,double>p_in;
    p_in = make_pair(sentence,sen_score);
    map_now[p_in] = make_pair(change_num,preopt + int2string(index) + " " + opt + " ");
}

void beam_search_delete_opt(string rawsentence, double rawscore, int pre_opt_num,string preopt,int index){
    pair<string,double>p_in;
    p_in = make_pair(rawsentence,rawscore + delete_score);
    map_now[p_in] = make_pair(pre_opt_num + 1,preopt + int2string(index) + " <D> ");
}

void beam_search_insert_opt(string nowchar,string rawsentence,double rawscore,int pre_opt_num,string suffixstr,string preopt, int index){
    set<string>new_insert_word = mytrie.find_prefix(rawsentence + nowchar);
    set<string>suffix_insert_word = mytrie.find_suffix(suffixstr);
    new_insert_word.insert(suffix_insert_word.begin(),suffix_insert_word.end());
    for(auto val : new_insert_word){
        string sentence = rawsentence + nowchar + val;
        get_new_map(sentence,rawscore, pre_opt_num + 1,insert_score,preopt,index,"<I>");
    }
}

void beam_search_replace_opt(string nowchar,string rawsentence,double rawscore,int pre_opt_num, string suffixstr,string preopt,int index){
    set<string>new_replace_word;
    vector<string> pinyin_replace_word = get_replace_word_from_pinyin(nowchar);
    new_replace_word.insert(pinyin_replace_word.begin(),pinyin_replace_word.end());

    set<string>prefix_replace_word = mytrie.find_prefix(rawsentence);
    set<string>suffix_replace_word = mytrie.find_suffix(suffixstr);
    new_replace_word.insert(prefix_replace_word.begin(),prefix_replace_word.end());
    new_replace_word.insert(suffix_replace_word.begin(),suffix_replace_word.end());

    for(auto val : new_replace_word){
        string sentence = rawsentence + val;
        get_new_map(sentence,rawscore, pre_opt_num + 1, replace_score,preopt,index,"<R>");
    }
    //debug_print("replace done");
}

string getsuffix(vector<string>tokens,int begin,int end){
    string str = "";
    for(int i = begin;i < end;i++){
        str += tokens[i];
    }
    return str;
}

map<pair<string,double>,pair<int,string>> beam_search(string encoder_context){
    map<pair<string,double>,pair<int,string>>map_pre;
    map<pair<string,double>,pair<int,string>>::iterator it; 
    pair<string,double>p_in;
    p_in = make_pair("<s>",0.0);
    map_pre[p_in] = make_pair(0,"");
    vector<string>tokens = chineseoneword(encoder_context);
    for(unsigned int i = 0; i < tokens.size();i++){
        string suffixstr = getsuffix(tokens,i + 1,tokens.size());
        string nowchar = tokens[i];
        int exclude_word_cnt = exclude_word.count(nowchar);
        int skip_length1 = singertrie.find_skip_length(nowchar + suffixstr,sentencesufix[i]);
        int skip_length2 = songtrie.find_skip_length(nowchar + suffixstr,sentencesufix[i]);
        int skip_length = max(max(skip_length1,skip_length2),exclude_word_cnt);
        if(skip_length != 0){
            map<pair<string,double>,pair<int,string>>map_tmp;
            string skipword = getsuffix(tokens,i,i + skip_length);
            //cout << "***"<<skip_length<<skipword<<endl; 
            for(it = map_pre.begin(); it != map_pre.end();it++){
                string rawsentence = it->first.first;
                if(rawsentence == "<s>") rawsentence = "";
                string sentence = rawsentence + skipword;
                double lmscore = get_lm_score(sentence,i);
                p_in = make_pair(sentence,it->first.second + no_change_score + lmscore);
                map_tmp[p_in] = it->second;
            }
            map_pre.clear();
            map_pre.insert(map_tmp.begin(),map_tmp.end());
            i += (skip_length - 1);
            continue;
        }
        //cout << "now word: " <<nowchar<<endl;
        map_now.clear();
        for(it = map_pre.begin(); it != map_pre.end();it++){
            //cout << it->first.first << " "<<it->first.second << " "<<it->second.first<<endl;
            string rawsentence = it->first.first;
            if (rawsentence == "<s>") rawsentence = "";
            string sentence = rawsentence + nowchar;
            double rawscore = it->first.second;
            int pre_opt_num = it->second.first;
            string preopt = it->second.second;
            //no opt 
            get_new_map(sentence,rawscore,pre_opt_num,no_change_score,preopt,i,"<N>");
            if(pre_opt_num < change_cnt){
                ///*delete opt 
                beam_search_delete_opt(rawsentence,rawscore,pre_opt_num,preopt,i);
                ///*insert opt: which word to insert
                beam_search_insert_opt(nowchar,rawsentence,rawscore,pre_opt_num,suffixstr,preopt,i);
                ///*replace opt 
                beam_search_replace_opt(nowchar,rawsentence,rawscore,pre_opt_num,suffixstr,preopt,i);
            }
        }
        map_pre.clear();
        int tmpcandidate = 0;
        for(it = map_now.begin();it != map_now.end();it++){
            map_pre.insert(*it);
            tmpcandidate += 1;
            if(tmpcandidate == candidate_cnt){
                break;
            }
        }
        if(map_now.begin()->first.second > not_process_score)
            break;
    }
    return map_pre;
}

pair<pair<string,double>,pair<int,string>>getpplscore(string sentence,double rawscore,pair<int,string>tmpp){
    string newsentence = getngramstring(sentence);
    pair<pair<string,double>,pair<int,string>>pout;
    pair<string,double>pin;
    double pplscore = mysrilm.getSentencePpl(newsentence);
    pin = make_pair(sentence,rawscore + pplscore); 
    pout = make_pair(pin,tmpp);
    return pout;
}

void write_res(string encoder_context,map<pair<string,double>,pair<int,string>>res){
    pair<pair<string,double>,pair<int,string>>pout;
    pair<string,double>pin;
    ofstream write;
    write.open(outputfilename,ios::app);
    if(!write.is_open()){
        cout<<"Output Open Error"<<endl;
        exit(1);
    }
    map<pair<string,double>,pair<int,string>>::iterator it;
    map<pair<string,double>,pair<int,string>>::iterator pre_it;
    map_now.clear();
    for(it = res.begin();it != res.end();){
        string sentence = it->first.first;
        double rawscore = it->first.second;
        //int optcnt = it->second.first;
        pout = getpplscore(sentence,rawscore,it->second);
        if(it == res.begin()){
            //map_now.insert(*it);
            map_now.insert(pout);
            pre_it = it;it++;continue;
        }
        if(it->first.first == pre_it->first.first)
           it = res.erase(it); 
        else{
            map_now.insert(pout);
            //map_now.insert(*it);
            pre_it = it;it++;
        }
    }
    int tmpcnt = 0;
    write<<encoder_context<<": " << "\t";
    if(int(chineseoneword(encoder_context).size()) < not_process_length or map_now.begin()->first.second > not_process_score){
        write<<encoder_context <<"  "<<"-1"<<" "<<"0";
    }
    else{
        for(it = map_now.begin(); it != map_now.end(); it++){
            write<<it->first.first<<"  "<<it->first.second<<" "<<it->second.first<<"  "<<it->second.second << "\t";
            tmpcnt += 1;
            if(tmpcnt == output_cnt) break;
        }
    }
    write<<endl;
    //write<<"-----------------------------"<<endl;
    //cout<<"********************"<<endl;
}

void fun_sentence_process(string encoder_context){
    //cout << "Process Sentence:" << encoder_context << endl;
    map<pair<string,double>,pair<int,string>> top_seq = beam_search(encoder_context);
    write_res(encoder_context,top_seq);
}

void get_similar_word(){ 
    map<char,string>similarchar = get_replace_char();
    multimap<string,string>::iterator it;
    multimap<string,string>::iterator itin;
    for(it = pinyin2word.begin(); it != pinyin2word.end(); it = pinyin2word.upper_bound(it->first)){
       string pinyin =  it->first;
       for(unsigned int i = 0; i < pinyin.length();i++){
           string replacepinyin = similarchar[pinyin[i]];
           for(auto val : replacepinyin){
               string tmpstr = "";
               tmpstr+=val;
               if(tmpstr == "") continue;
               string nowpinyin = pinyin;
               nowpinyin = nowpinyin.replace(i,1,tmpstr);
               if(pinyin2word.find(nowpinyin) != pinyin2word.end()){
                  itin = pinyin2word.find(nowpinyin);
                  multimap<string,string>tmppinyin;
                  tmppinyin.clear();
                  for(unsigned int  k = 0; k!= pinyin2word.count(nowpinyin);k++,itin++){
                      tmppinyin.insert(make_pair(pinyin,itin->second));
                  }
                  pinyin2word.insert(tmppinyin.begin(),tmppinyin.end());
               }
           }
       }
    }
}

void getsentencesufix(string sentence){
    vector<string>tokens = chineseoneword(sentence);
    sentencesufix.clear();
    for(int i = 0;i < int(tokens.size()); i++){
        string tmpstr = "";
        vector<string>tmp;
        tmp.clear();
        for(int j = i+1; j < int(tokens.size());j++){
            tmpstr += tokens[j];
            tmp.push_back(tmpstr);
        }
        sentencesufix.push_back(tmp);
    }
}

void fun_getinput(){
    string line;
    ifstream replacedictfile(dictreplacefilename);
    if (!replacedictfile.is_open()){
        cout<<"replacedictfile Open Error"<<endl;
        exit(1);
    }
    while(getline(replacedictfile,line)){
        string rawsentence = convchinese(line);
        vector<string>sp = split(rawsentence," ");
        string word = sp[0];
        string pinyin = sp[1];
        word2pinyin[word] = pinyin;
        pinyin2word.insert(pair<string,string>(pinyin,word));
    }
    get_similar_word();
    ifstream songdictfile(songfilename);
    if(!songdictfile.is_open()){
        cout<<"songdictfile Open Error"<<endl;
        exit(1);
    }
    while(getline(songdictfile,line)){
        string rawsentence = convchinese(line);
        mytrie.insert_prefix(rawsentence);
        mytrie.insert_suffix(rawsentence);
        songtrie.insert_name(rawsentence);
    }

    ifstream singerdictfile(singerfilename);
    if(!singerdictfile.is_open()){
        cout<<"Singerfile Open Error";
        exit(1);
    }
    while(getline(singerdictfile,line)){
        string sentence = convchinese(line);
        singertrie.insert_name(sentence);
    }
    //singertrie.print_all();
    //singertrie.print_one("李");
    //mytrie.print_all();
    ifstream inputfile(inputfilename);
    if (!inputfile.is_open()){
        cout<<"Input Open Error"<<endl;
        exit(1);
    }
    time_t t_start, t_end;
    t_start = time(NULL);
    int tmpprintcnt = -1;
    while(getline(inputfile, line)){
        //cout << line <<endl;
        tmpprintcnt += 1;
        string rawsentence = convchinese(line);
        //cout<<rawsentence<<endl;
        if(tmpprintcnt % 100 == 0){
            cout << tmpprintcnt <<" "<<rawsentence<<endl;
        }
        if(int(chineseoneword(rawsentence).size()) < not_process_length){
            map<pair<string,double>,pair<int,string>>map_pre;
            map_pre.clear();
            write_res(rawsentence,map_pre);
        }
        else{
            getsentencesufix(rawsentence);
            fun_sentence_process(rawsentence);
        }
    }
    t_end = time(NULL);
    cout<<"**Process Time: "<<difftime(t_end,t_start)<<endl;
}

int main(int argc, char* argv[]){
    inputfilename = argv[1];
    dictreplacefilename = argv[2];
    songfilename = argv[3];
    lmfilename = argv[4];
    singerfilename = argv[5];
    outputfilename = argv[6];
    n_gram = atoi(argv[7]);
    change_cnt = atoi(argv[8]);
    insert_score = atof(argv[9]);
    delete_score = atof(argv[10]);
    replace_score = atof(argv[11]);
    no_change_score = atof(argv[12]);
    candidate_cnt = atoi(argv[13]);
    output_cnt = atoi(argv[14]);
    not_process_length = atoi(argv[15]);
    not_process_score = atoi(argv[16]);

    //stream << output_cnt;
    //string tmpstr;
    //stream >> tmpstr;
    string tmpinputfilename = split(inputfilename,"/")[1];
    strcat(outputfilename,(char*)tmpinputfilename.data());
    strcat(outputfilename,"_out_");
    strcat(outputfilename,(char*)int2string(output_cnt).data());
    //cout << outputfilename<<endl;
    if(access(outputfilename,F_OK) == 0){
        remove(outputfilename);
    }
    mysrilm.set_srilm(n_gram,lmfilename);
    fun_getinput();
    return 0;
}
