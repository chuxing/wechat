DATADIR=$1

FASTTEXT_BIN=../fasttext

${FASTTEXT_BIN} supervised -input "fast.train" -output "fast.model" -dim 50 -lr 0.015 -wordNgrams 3 -minCount 6 -bucket 100000 -epoch 50 -thread 8 -loss softmax
#${FASTTEXT_BIN} supervised -input "fast.train" -output "fast.model" -dim 300 -lr 0.015 -wordNgrams 3 -minCount 10 -bucket 100000 -epoch 100 -thread 8 -loss softmax

#echo "test on train set: " `${FASTTEXT_BIN} test "fast.model.bin" "fast.train"`
echo "test on test set: "  `${FASTTEXT_BIN} test "fast.model.bin" "fast.test"`

${FASTTEXT_BIN} predict "fast.model.bin" "fast.test" > "fast.test.predict"

python viewResult.py "fast.test" "fast.test.predict" > eval_result.txt
python ./record_errors.py ./fast.test.predict ./fast.test
python ./cnt_and_remove_record.py ./record_flip_label_data.txt ./fast.test
