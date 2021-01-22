infolder=$1
outdir=${infolder}_uniq

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	uniq  ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}
 	(( i++ ))
done