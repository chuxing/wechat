#ifndef TEXT_H
#define TEXT_H
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;
class Text
{
    protected:
        char * m_binaryStr;
        size_t m_length;
        size_t m_index;
    public:
        Text(string str);
        void setIndex(size_t index);
        virtual int ReadOneChar(string &oneChar) = 0;
        virtual vector<string> tokenize() = 0;
        size_t size();
        virtual ~Text();
};
#endif
