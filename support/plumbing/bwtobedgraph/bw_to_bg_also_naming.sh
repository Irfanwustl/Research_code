

cram_in=$1

outdir=${cram_in}_bg

dirList=($( ls $cram_in ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	./bigWigToBedGraph ${cram_in}/${dirList[i]}/build*/results/cpgs.bw ${outdir}/${dirList[i]}.bedgraph  
 	(( i++ ))
done