#ifndef TEXTFACTORY_H
#define TEXTFACTORY_H
#include <iostream>
#include "Text.h"
#include "UtfText.h"
#include "GbkText.h"
using namespace std;
class TextFactory
{
    public:
        static Text * CreateText(string textCode, string str);
};
#endif
