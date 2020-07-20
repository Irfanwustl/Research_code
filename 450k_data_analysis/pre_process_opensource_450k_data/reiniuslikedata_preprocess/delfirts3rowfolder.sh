infolder=$1
outdir=${infolder}_first3deleted

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	tail -n +4 ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}
 	(( i++ ))
done