#ifndef GBKTEXT_H
#define GBKTEXT_H
#include <iostream>
#include <string>
#include "Text.h"
using namespace std;
class GbkText:public Text
{
public:
    GbkText(string str);
    ~GbkText(void);
    int ReadOneChar(string & oneChar); // return the number of bytes of this oneChar
    vector<string> tokenize();
};
#endif
