start=$SECONDS

infolder=$1

howmany=$2

outdir=${infolder}_rankedwithv4

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 hypo_meth_cutoffv2_withv4.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]} ${howmany}
 	(( i++ ))
done


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

