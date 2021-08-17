

bamfolder=$1

outdir=$2

dirList=($( ls $bamfolder ))




i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools calmd -b  ${bamfolder}/${dirList[i]} /home/ialahi/work/plumbing/all_sequences.fa > ${outdir}/${dirList[i]}_mdadded.bam
 	(( i++ ))
done