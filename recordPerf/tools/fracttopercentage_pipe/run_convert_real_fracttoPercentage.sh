start=$SECONDS

infolder=$1
outdir=${infolder}_gtpercentage

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do
	echo now=========${dirList[i]} 
	python3 convert_real_fracttoPercentage.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}

	(( i++ ))
done

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
