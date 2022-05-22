start=$SECONDS

fol=$1
mergedfolder=${fol}_formatted2
interfol=${fol}_inter2



mkdir ${mergedfolder}
mkdir ${interfol}




dirList=($( find ${fol} -maxdepth 1 -type f -not -path '*/\.*'))

parallel -j 8 python3 ENCODE_formatter2.py ::: ${dirList[@]} ::: ${mergedfolder} ::: ${interfol}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
