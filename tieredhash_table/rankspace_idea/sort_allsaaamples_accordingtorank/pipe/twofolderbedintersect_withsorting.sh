start=$SECONDS

folderA=$1
folderB=$2
outfolder=${folderA}_int_${folderB}

dirList=($( ls ${folderA} ))






mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	./bedintersect_onefolder.sh ${folderA}/${dirList[i]} ${folderB} ${outfolder}

	(( i++ ))

done


python3 sort_sample_accordingtorank.py ${outfolder} ${folderB}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


