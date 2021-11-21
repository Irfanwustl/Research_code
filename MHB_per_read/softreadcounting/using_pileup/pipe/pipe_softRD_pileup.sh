start=$SECONDS





bamfolder=$1
smfile=$2




outdir=${bamfolder}_softRDpileup

dirList=($( ls ${bamfolder} | grep -v '\.bai$'))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	

	python3 softRD_pileup.py ${bamfolder}/${dirList[i]} ${smfile}  ${outdir}/${dirList[i]} 

	(( i++ ))
done



python3 combineresult_formergingwithgt.py ${outdir}




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


