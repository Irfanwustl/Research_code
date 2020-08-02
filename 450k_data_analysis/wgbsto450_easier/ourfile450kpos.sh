
sigPos=$1 #####Not sig actually, 450k pos. 

mixin=$2 

outdir=${mixin}_${sigPos}_intersected
mkdir ${outdir}

dirList=($( ls ${mixin}  ))



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	


	bedtools intersect -u -wa -a ${mixin}/${dirList[i]} -b ${sigPos}  > ${outdir}/${dirList[i]} 
 	(( i++ ))
done