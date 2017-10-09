#include "Text.h"
using namespace std;
Text::Text(string str):m_index(0) 
{
  m_length = str.size();
  m_binaryStr = new char[m_length+1];
  str.copy(m_binaryStr, m_length);
}

void Text::setIndex(size_t index)
{
    m_index = index;
}

size_t Text::size()
{
    return m_length;
}

Text::~Text()
{
    delete [] m_binaryStr;
}
