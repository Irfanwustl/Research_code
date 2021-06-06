infolder=$1
outdir=${infolder}_bam

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools view -h -b ${infolder}/${dirList[i]}  -o ${outdir}/${dirList[i]}.bam
 	(( i++ ))
done