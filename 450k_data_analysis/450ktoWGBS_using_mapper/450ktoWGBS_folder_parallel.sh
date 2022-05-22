start=$SECONDS


dir=$1
coretouse=$2
outfol=${dir}_WGBSparallel
mkdir ${outfol}

dirList=($( find ${dir} -maxdepth 1 -type f -not -path '*/\.*'))

parallel -j ${coretouse} python3 450ktoWGBS_forparallel.py ::: ${dirList[@]} ::: ${outfol}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
