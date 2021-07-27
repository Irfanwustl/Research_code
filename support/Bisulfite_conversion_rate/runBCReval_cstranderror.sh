start=$SECONDS


infolder=$1
outdir=${infolder}_BCR

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 

	outname=${dirList[i]}_BCR.txt

	

	python BCReval_cstranderror.py -n 10 -i ${infolder}/${dirList[i]}  -o ${outdir}/${outname}
	
 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

