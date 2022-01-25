infolder=$1
intwith=$2

intwithbase=$( basename ${intwith} )

outdir=$3 #${infolder}_intersectedwith_${intwithbase}


dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -wa -wb -a ${infolder}/${dirList[i]} -b ${intwith} > ${outdir}/${dirList[i]}_${intwithbase}.txt 
 	(( i++ ))
done