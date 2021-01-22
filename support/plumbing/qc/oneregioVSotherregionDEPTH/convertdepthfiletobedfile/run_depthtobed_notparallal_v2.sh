start=$SECONDS

infodepthfolder=$1

outfolder=${infodepthfolder}_bed


mkdir ${outfolder}

dirList=($( ls ${infodepthfolder}  ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	
	python3 depthtobed_notparallal_v2.py ${infodepthfolder}/${dirList[i]} ${outfolder}/${dirList[i]}.bed
 	(( i++ ))
done




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
