DATADIR=$1

FASTTEXT_BIN=~/code/fasttext/fasttext

${FASTTEXT_BIN} supervised -input "fast.train" -output "fast.model" -dim 50 -lr 0.015 -wordNgrams 3 -minCount 6 -bucket 100000 -epoch 50 -thread 8 -loss softmax

echo "test on train set: " `${FASTTEXT_BIN} test "fast.model.bin" "fast.train"`
echo "test on test set: "  `${FASTTEXT_BIN} test "fast.model.bin" "fast.test"`

${FASTTEXT_BIN} predict "fast.model.bin" "fast.test" > "fast.test.predict"

python viewResult.py "fast.test" "fast.test.predict" > eval_result.txt
