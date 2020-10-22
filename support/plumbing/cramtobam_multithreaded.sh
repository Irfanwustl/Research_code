

cram_in=$1 #model_data

outdir=${cram_in}_bam

dirList=($( ls $cram_in ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools view -b -T /home/ialahi/work/plumbing/all_sequences.fa -o $outdir/${dirList[i]}.final.bam  -@ 8 ${cram_in}/${dirList[i]}/build*/results/final.cram 
 	(( i++ ))
done