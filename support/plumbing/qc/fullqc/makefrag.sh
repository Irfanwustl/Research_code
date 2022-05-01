#! /bin/bash


dir=$1 #some_bam_onlyunmapped
outdir="${dir}_frag"
mkdir  ${outdir}


dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do
	echo now=========${dirList[i]}

	samtools view -@ 8  ${dir}/${dirList[i]} | awk '{print $9}' > $outdir/${dirList[i]}_frag

	(( i++ ))
done




echo "now R ...."

frag_img=${outdir}_frag_img

mkdir ${frag_img}

Rscript frag_pp.R ${outdir} ${frag_img}