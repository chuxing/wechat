#########################################################################
# File Name: run.sh
# Author: letian
# Mail: @.com
# Created Time: Tue 21 Mar 2017 10:19:37 PM CST
#########################################################################

result=result
FASTTEXT_BIN=./fasttext

mkdir $result

let number=10

for((t=1; t<=number; t++))
do
    let pre=t-1
    python rand_k_valid.py $result/raw_data.txt.v${pre} $number> $result/raw_data.txt.v${pre}.k${number}.r${t}
    #python rand_k_valid.py all_train.txt > $c_v_fold/all_train.txt.k10

    for ((i=0; i<number; i++))
    do
        # split corpus
        python create_corpus.py $i $result/raw_data.txt.v${pre}.k${number}.r${t} $result # generate "train.txt" "test.txt"
        # train model
        $FASTTEXT_BIN supervised -input $result/train.txt -output $result/fast.model -dim 30 -lr 0.015 -wordNgrams 3 -minCount 5 -bucket 100000 -epoch 15 -thread 8 -loss softmax
        # predict
        $FASTTEXT_BIN predict "$result/fast.model.bin" "$result/test.txt" > "$result/test.pred"
        # viewresult
        python viewResult.py $result/test.txt $result/test.pred > $result/eval_res_${t}
        # retest
        python re_create_raw.py "$result/test.pred"  "$result/test.txt"  "$result/raw_data.txt.v$t"  $t $result 
    done
done

cat $result/eval_res_* > $result/eval_res.txt
cat $result/record_flip_label_data.txt.v* > $result/record_flip_label_data.txt
# result file save in record_flip_label_data.txt.s and raw_data.txt.v0.s
python cnt_and_remove_record.py $result/record_flip_label_data.txt $result/raw_data.txt.v0
