
cram_in=$1 #model_data

outdir=${cram_in}_bed

dirList=($( ls $cram_in ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	zcat ${cram_in}/${dirList[i]}/build*/results/cpgs.bed.gz > ${outdir}/${dirList[i]}.bed 
 	(( i++ ))
done