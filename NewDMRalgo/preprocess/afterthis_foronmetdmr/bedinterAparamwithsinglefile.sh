infolder=$1
intwith=$2
outdir=${infolder}_intersectedwith_paramA_$( basename ${intwith} )

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -wa -wb -a ${intwith}  -b ${infolder}/${dirList[i]} -header > ${outdir}/${dirList[i]} 
 	(( i++ ))
done
