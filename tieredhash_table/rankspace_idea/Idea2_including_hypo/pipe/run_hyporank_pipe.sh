start=$SECONDS

rowfile=$1

deltainfofolder=$2

howmany=$3


outdir=${deltainfofolder}_betaInfo

dirList=($( ls ${deltainfofolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 bedintersectlike.py  ${rowfile}   ${deltainfofolder}/${dirList[i]} ${outdir}/${dirList[i]}

	python3 Ranking_from_rankspace_withHYPO_HARDCODEDgroupinfo.py ${outdir}/${dirList[i]} ${outdir}/${dirList[i]} ${howmany}

 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



