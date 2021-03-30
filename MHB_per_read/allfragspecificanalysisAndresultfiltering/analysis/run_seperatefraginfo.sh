start=$SECONDS

infolder=$1 # final file dir

outdir=$2

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 seperatefraginfo.py ${infolder}/${dirList[i]} ${outdir}
 	(( i++ ))
done


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

