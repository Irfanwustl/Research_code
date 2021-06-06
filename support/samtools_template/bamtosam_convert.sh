infolder=$1
outdir=${infolder}_sam

dirList=($( ls ${infolder} | grep -v '\.bai$' ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools view -h ${infolder}/${dirList[i]}  -o ${outdir}/${dirList[i]}_sam.txt
 	(( i++ ))
done