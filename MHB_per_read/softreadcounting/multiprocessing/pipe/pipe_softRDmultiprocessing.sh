start=$SECONDS





bamfolder=$1
smfile=$2

coretouse=$3




outdir=${bamfolder}_softMultiprocessing

dirList=($( ls ${bamfolder} | grep -v '\.bai$'))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	

	python3 softRDmultiprocessing.py ${bamfolder}/${dirList[i]} ${smfile}  ${outdir}/${dirList[i]} ${coretouse}

	(( i++ ))
done



python3 combineresult_formergingwithgt.py ${outdir}




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


