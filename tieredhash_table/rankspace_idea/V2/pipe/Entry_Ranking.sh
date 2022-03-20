start=$SECONDS

infolder=$1

howmany=$2



dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	

	python3 Ranking_from_rankspace_v2_HARDCODEDgroupinfo.py ${infolder}/${dirList[i]} ${howmany}
 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

