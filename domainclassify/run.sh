#########################################################################
# File Name: run.sh
# Author: 
# Mail: @.com
# Created Time: Tue 23 May 2017 11:35:44 AM CST
#########################################################################
#!/bin/bash

cat train_music.txt train_movie.txt train_weather.txt train_remind.txt train_news.txt > fast.train

cp fast.train all_train.txt
cp fast.train fast.test

./cross_validation.sh
./classification.token.sh
