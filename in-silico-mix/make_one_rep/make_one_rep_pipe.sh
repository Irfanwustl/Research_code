

infolder=$1
extension=$2
outdir=${infolder}_onerep

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 

	celllist=($( find ${infolder}/${dirList[i]} -type f -name *${extension} ))

	samtools merge -@ 20 ${outdir}/${dirList[i]}.bam  ${celllist[@]}

	
 	(( i++ ))
done