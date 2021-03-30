

bamfolder=$1

outdir=${bamfolder}_mdadded

dirList=($( ls $bamfolder ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools calmd -b  ${bamfolder}/${dirList[i]} /home/ialahi/work/plumbing/all_sequences.fa > ${outdir}/${dirList[i]}_mdadded.bam
 	(( i++ ))
done