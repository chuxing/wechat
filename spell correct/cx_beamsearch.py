#!/usr/bin/python  
#-*- coding:utf-8 -*-  
#######################################################  
#File Name: beamsearch.py
#Author: Chu Xing
#Mail: v_xingzhu@tencent.com  
#Created Time: 2017-07-20 17:41:22
########################################################  
from __future__ import unicode_literals
import sys
import codecs
import os
import numpy as np
import random
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Seven Chu'
vocab = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'BOS',
        6: 'EOS'
        }
reverse_vocab = dict([(v,k) for k,v in vocab.items()])
vocab_size = len(vocab.items())
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
def reduce_mul(l):
    out = 1.0
    for x in l:
        out *= x
    return out 

def check_all_done(seqs):
    for seq in seqs:
        if not seq[-1]:
            return False 
    return True 

def decode_step(encoder_context, input_seq):
    print encoder_context,input_seq 
    #encoder_context contains informaion of encoder
    #ouput_step contains the words' probability
    #these two varibles should be generated by seq2seq model
    words_prob = [random.random() for _ in range(vocab_size)]
    words_prob[reverse_vocab['BOS']] = 0.0
    words_prob = softmax(words_prob)
    ouput_step = [(idx,prob) for idx,prob in enumerate(words_prob)]        
    ouput_step = sorted(ouput_step, key=lambda x: x[1], reverse=True)
    return ouput_step

#seq: [[word,word],[word,word],[word,word]]
#output: [[word,word,word],[word,word,word],[word,word,word]]

def beam_search_step(encoder_context, top_seqs, k):
    all_seqs = []
    for seq in top_seqs:
        print seq
        seq_score = reduce_mul([_score for _,_score in seq])
        if seq[-1][0] == reverse_vocab['EOS']:
            all_seqs.append((seq, seq_score, True))
            continue
        #get current step using encoder_context & seq
        current_step = decode_step(encoder_context, seq)
        for i,word in enumerate(current_step):
            if i >= k:
                break 
            word_index = word[0]
            word_score = word[1]
            score = seq_score * word_score
            rs_seq = seq + [word]
            done = (word_index == reverse_vocab['EOS'])
            all_seqs.append((rs_seq, score, done))            
    all_seqs = sorted(all_seqs, key = lambda seq: seq[1], reverse=True)
    topk_seqs = [seq for seq,_,_ in all_seqs[:k]]
    all_done = check_all_done(all_seqs)
    return topk_seqs, all_done 

def beam_search(encoder_context):
    beam_size = 3
    max_len = 10
    #START
    top_seqs = [[(reverse_vocab['BOS'],1.0)]]
    #loop 
    for _ in range(max_len):
        top_seqs, all_done = beam_search_step(encoder_context, top_seqs, beam_size)
        if all_done:
            break 
    return top_seqs 

if __name__ == '__main__':
    encoder_context = "hello" 
    top_seqs = beam_search(encoder_context)
    for i,seq in enumerate(top_seqs):
        print 'Path[%d]: ' % i
        for word in seq[1:]:
            word_index = word[0]
            word_prob = word[1]
            print '%s(%.4f)' % (vocab[word_index], word_prob),
            if word_index == reverse_vocab['EOS']:
                break 
        print '\n'
