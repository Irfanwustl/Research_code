start=$SECONDS

infolder=$1
outdir=${infolder}_informative

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do
	echo now=========${dirList[i]} 
	python3 onlyinformative.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}

	(( i++ ))
done

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
