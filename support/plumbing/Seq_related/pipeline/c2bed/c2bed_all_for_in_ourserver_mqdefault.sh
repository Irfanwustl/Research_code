

#bsub -M 48000000 -R 'select[mem>48000] span[hosts=1] rusage[mem=48000]' -oo MAPQ0_filtered_all.err -q research-hpc -a "docker(mgibio/biscuit)" -J irffinaling "bash c2bed_all_for.sh"


###input folder er last e sorted thaka jabe na

start=$SECONDS

out_folder=all_outputs

set -eo pipefail



file_directory="test_bam_sorted_renameforc2bed"
outdir="${file_directory}_mdefault_Bedout"


mkdir  ${outdir}


fList=($( find ${file_directory} -name "*_sorted"  ))

cores=35

echo ${fList[@]}

for fl in ${fList[@]}
do
	echo "loop start....."
	fin=$(basename ${fl})
	echo ${fin} 

	biscuit pileup -q $cores -w ${outdir}/${fin}_pileup.txt -o ${outdir}/${fin}_pileup.txt  /home/ialahi/software/all_sequences.fa ${file_directory}/${fin}

	echo "pileup done"

	bgzip --threads $cores ${outdir}/${fin}_pileup.txt 



	echo "bgzip done"

	biscuit vcf2bed -t cg -k 1 -e ${outdir}/${fin}_pileup.txt.gz | biscuit mergecg /home/ialahi/software/all_sequences.fa /dev/stdin -k 2 |  tee >(/bin/gzip >${outdir}/${fin}_cpg.gz) | cut -f 1-4 | sort -k1,1 -k2,2n -S 12G | /usr/bin/perl -ne 'print $_ if $_ =~ /^(chr)?[1-9]?[0-9|X|Y]\s/' > ${outdir}/${fin}_cpg.bedgraph
	
	
	echo "bedgraph done. new satrting...."

done


for i in 1 2 3 4 5
do
   echo "Welcome $i times"
done

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"