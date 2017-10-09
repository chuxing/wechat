#include "GbkText.h"
GbkText::GbkText(string str):Text(str){}
GbkText::~GbkText(void) {}
int GbkText::ReadOneChar(string & oneChar)
{
    if(m_length == m_index)
        return 0;
    if((unsigned char)m_binaryStr[m_index] < 0x81)
    {
        oneChar = m_binaryStr[m_index];
        m_index++;
        return 1;
    }
    else
    {
        oneChar = string(m_binaryStr + m_index, 2);
        m_index += 2;
        return 2;
    }
}

vector<string> GbkText::tokenize(void) {
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
