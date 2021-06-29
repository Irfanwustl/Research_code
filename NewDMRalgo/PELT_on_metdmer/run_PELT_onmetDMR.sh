start=$SECONDS

infolder=$1
penaltyvalue=$2 #3.5 
percoreMetDMR=$3 #1000

minCpG=3


outdir=${infolder}_PELT_minsegesize_${minCpG}_penaltyvalue_${penaltyvalue}_percoreMetDMR_${percoreMetDMR}

seginfooutdir=${outdir}_segmentinfo

dirList=($( ls ${infolder}  ))



mkdir ${outdir}

mkdir ${seginfooutdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo nowPELT=========${dirList[i]} 

	python3 PELT_onmetDMR2_childrencorr.py ${infolder}/${dirList[i]} ${minCpG} ${penaltyvalue} ${percoreMetDMR}  ${outdir}/${dirList[i]}  ${seginfooutdir}/${dirList[i]}
 	(( i++ ))
done


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

