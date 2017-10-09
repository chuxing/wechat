#!/bin/bash --login
alias pythona2=~/Software/anaconda2/bin/python2
shopt expand_aliases   
shopt -s  expand_aliases 
shopt expand_aliases   
pythona2 ./ss_news.py "./data/" "unlabeldata"
