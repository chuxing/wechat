#########################################################################
# File Name: run.sh
# Author: kano
# Mail: @.com
# Created Time: Tue 21 Mar 2017 10:19:37 PM CST
#########################################################################

chmod +x fasttext

for ((t=1; t<=10; t++))
do
    let pre=t-1
    # random generate 10 cvs
    python rand_k_valid.py raw_data.txt.v${pre} > raw_data.txt.v${pre}.k10.r${t}

    for ((i=0; i<10; i++))
    do
        # split corpus
        python create_corpus.py $i raw_data.txt.v${pre}.k10.r${t} # generate "train.txt" "test.txt"
        # train model
        ./fasttext supervised -input train.txt -output model -dim 30 -lr 0.015 -wordNgrams 3 -minCount 5 -bucket 100000 -epoch 15 -thread 8 -loss softmax
        # predict
        ./fasttext predict "model.bin" "test.txt" > "test.pred"
        # viewresult
        python viewResult.py test.txt test.pred
        # retest
        python re_create_raw.py test.pred  test.txt  raw_data.txt.v$t  $t # 追加写

    done

done

cat record_flip_label_data.txt.v* > record_flip_label_data.txt

# result file save in record_flip_label_data.txt.s and raw_data.txt.v0.s
python cnt_and_remove_record.py record_flip_label_data.txt raw_data.txt.v0

