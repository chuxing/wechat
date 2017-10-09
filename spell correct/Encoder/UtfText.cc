#include "UtfText.h"
UtfText::UtfText(string str):Text(str){}
UtfText::~UtfText(void) {}
int UtfText::ReadOneChar(string & oneChar)
{
    if(m_length == m_index)
        return 0;
    size_t utf8_char_len = get_utf8_char_len(m_binaryStr[m_index]);
    if( 0 == utf8_char_len )
    {
        oneChar = "";
        m_index++;
        return -1;  // means this byte is error
    }
    size_t next_idx = m_index + utf8_char_len;
    if( m_length < next_idx )
    {
        //cerr << "Get utf8 first byte out of input src string." << endl;
        next_idx = m_length;
    }
    //输出UTF-8的一个字符
    oneChar = string(m_binaryStr + m_index, next_idx - m_index);
    //重置偏移量
    m_index = next_idx;
    return utf8_char_len;
}

vector<string> UtfText::tokenize() {
  // keep state
  size_t index = m_index;
  vector<string> res;
  string word;
  while (ReadOneChar(word) != 0)
    res.push_back(word);
  // restore state
  m_index = index;
  return res;
}

size_t UtfText::get_utf8_char_len(const char & byte)
{
    // return 0 表示错误
    // return 1-6 表示正确值
    // 不会 return 其他值

    //UTF8 编码格式：
    //     U-00000000 - U-0000007F: 0xxxxxxx
    //     U-00000080 - U-000007FF: 110xxxxx 10xxxxxx
    //     U-00000800 - U-0000FFFF: 1110xxxx 10xxxxxx 10xxxxxx
    //     U-00010000 - U-001FFFFF: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
    //     U-00200000 - U-03FFFFFF: 111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
    //     U-04000000 - U-7FFFFFFF: 1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx

    size_t len = 0;
    unsigned char mask = 0x80;
    while( byte & mask )
    {
        len++;
        if( len > 6 )
        {
            //cerr << "The mask get len is over 6." << endl;
            return 0;
        }
        mask >>= 1;
    }
    if( 0 == len)
    {
        return 1;
    }
    return len;
}
