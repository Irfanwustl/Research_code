start=$SECONDS #/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/cd4binnstatsfiles





bamfolder=$1





outdir=${bamfolder}_rebindiffdelta

dirList=($( ls ${bamfolder} | grep -v '\.bai$'))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	

	python3 rebinning_differentdelta.py ${bamfolder}/${dirList[i]}  ${outdir}/${dirList[i]} 

	(( i++ ))
done



#python3 combineresult_formergingwithgt.py ${outdir}




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


