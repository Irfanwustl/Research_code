infolder=$1
intwith=$2
outdir=${infolder}_intersectedwith_${intwith}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -wa -wb -a ${infolder}/${dirList[i]} -b ${intwith} > ${outdir}/${dirList[i]} 
 	(( i++ ))
done