#ifndef UTFTEXT_H
#define UTFTEXT_H
#include <iostream>
#include <string>
#include "Text.h"
using namespace std;
class UtfText:public Text
{
public:
    UtfText(string str);
    ~UtfText(void);
    int ReadOneChar(string & oneChar);
    vector<string> tokenize();
private:
    size_t get_utf8_char_len(const char & byte);
};
#endif
