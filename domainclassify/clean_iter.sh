#########################################################################
# File Name: clean_iter.sh
# Author: 
# Mail: @.com
# Created Time: Mon 27 Feb 2017 06:43:30 PM CST
#########################################################################
#!/bin/bash

i=$1

# ./classification.token.sh 
# ./../../../../fasttext/fasttext supervised -input "fast.train" -output "fast.model" -dim 50 -lr 0.015 -wordNgrams 3 -minCount 6 -bucket 100000 -epoch 50 -thread 8 -loss softmax

#./../../../../fasttext/fasttext predict "fast.model.bin" fast.train > fast.train.predict

sed -i 1d fast.train.predict

paste fast.train.predict fast.train | grep "^__label__music" | grep __label__chat | cut -f 2 | sed "s/__label__chat/__label__music/g" > music_in_chat.txt.v${i}
paste fast.train.predict fast.train | grep "^__label__chat" | grep -v __label__music | cut -f 2 > chat_in_chat.txt.v${i}

cat train_news.txt chat_in_chat.txt.v${i} > raw_data.txt.v${i}

cp raw_data.txt.v${i}  fast.train
# python oversampling_balance_data.py raw_data.txt.v${i} fast.train

