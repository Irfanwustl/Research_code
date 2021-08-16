infolder=$1
outdir=$2

dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools view -b -F 4 ${infolder}/${dirList[i]}  -o ${outdir}/${dirList[i]}
 	(( i++ ))
done