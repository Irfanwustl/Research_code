start=$SECONDS


infolder=$1


outdir=${infolder}_linecount

dirList=($( ls ${infolder}  ))


mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 Shoonhsin_linecount.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}
 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

