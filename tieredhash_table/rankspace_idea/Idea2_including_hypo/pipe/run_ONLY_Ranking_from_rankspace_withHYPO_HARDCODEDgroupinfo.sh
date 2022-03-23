start=$SECONDS



deltainfofolder=$1 #deltainfofolder_betaInfo

howmany=$2




dirList=($( ls ${deltainfofolder}  ))



outdir=${deltainfofolder}_RANKED

mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	

	python3 Ranking_from_rankspace_withHYPO_HARDCODEDgroupinfo.py ${deltainfofolder}/${dirList[i]} ${outdir}/${dirList[i]} ${howmany}

 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



