#include "TextFactory.h"
#include "Text.h"
Text * TextFactory::CreateText(string textCode, string str)
{
    if( (textCode == "utf-8")
                || (textCode == "UTF-8")
                || (textCode == "ISO-8859-2")
                || (textCode == "ascii")
                || (textCode == "ASCII")
                || (textCode == "TIS-620")
                || (textCode == "ISO-8859-5")
                || (textCode == "ISO-8859-7") )
    {
        return new UtfText(str);
    }
    else if((textCode == "windows-1252")
                || (textCode == "Big5")
                || (textCode == "EUC-KR")
                || (textCode == "GB2312")
                || (textCode == "ISO-2022-CN")
                || (textCode == "HZ-GB-2312")
                || (textCode == "gb18030"))
    {
        return new GbkText(str);
    }
    return NULL;
}
