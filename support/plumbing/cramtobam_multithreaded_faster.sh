

cram_in=$1 #model_data

outdir=${cram_in}_bam

dirList=($( ls $cram_in ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	cp ${cram_in}/${dirList[i]}/build*/results/final.cram /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.cram

	samtools view -b -T /home/ialahi/work/plumbing/all_sequences.fa -o /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.bam  -@ 30 /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.cram

	cp /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.bam ${outdir}/

	rm /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.cram
	rm /logo2/ialahi2/irftmp/cramtobam/${dirList[i]}.final.bam

 	(( i++ ))
done