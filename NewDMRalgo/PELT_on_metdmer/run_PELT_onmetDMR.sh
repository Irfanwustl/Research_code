infolder=$1
penaltyvalue=$2 #3.5 
percoreMetDMR=$3 #1000

minCpG=3


outdir=${infolder}_PELT_minsegesize_${minCpG}_penaltyvalue_${penaltyvalue}_percoreMetDMR_${percoreMetDMR}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo nowPELT=========${dirList[i]} 

	python3 PELT_onmetDMR.py ${infolder}/${dirList[i]} ${minCpG} ${penaltyvalue} ${percoreMetDMR}  ${outdir}/${dirList[i]} 
 	(( i++ ))
done