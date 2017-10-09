python ./get_new_data.py ./unlabeldata ./labeldata newulabeldata same 
echo "get_new_data done"
mv newulabeldata unlabeldata
python ./random_split.py labeldata 0.8
mv *0.8 train
mv *0.2 valid
