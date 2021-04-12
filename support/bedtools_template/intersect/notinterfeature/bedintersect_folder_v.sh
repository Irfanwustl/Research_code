infolder=$1
intwith=$2
outdir=${infolder}_nointersectedwith_${intwith}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -a ${infolder}/${dirList[i]}  -b ${intwith} -v > ${outdir}/${dirList[i]} 
 	(( i++ ))
done