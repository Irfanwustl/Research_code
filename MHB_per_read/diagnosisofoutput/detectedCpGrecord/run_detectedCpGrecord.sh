infolder=$1 #masterdf or finaldf.like: /Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/readbaseddecon3/postanalysis/forheatmap/datain
ref=$2
outdir=${infolder}_cpgrecord

dirList=($( ls ${infolder} ))

echo ${dirList[@]}



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 detectedCpGrecord.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done

python3 combineAlldf.py ${outdir} ${outdir}_combined.txt



python3 compatibleSM.py ${ref}  ${ref}_compatible.txt


python3 mergewithref.py ${ref}_compatible.txt ${outdir}_combined.txt ${outdir}_combinedmergedwithSM.txt




