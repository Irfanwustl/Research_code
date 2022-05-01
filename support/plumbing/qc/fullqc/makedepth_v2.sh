#! /bin/bash


dir=$1

prefix=$2

tempdir=${dir}_depthfullinfo
mkdir ${tempdir}

outdir="${dir}_depth"
mkdir  ${outdir}




dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do

	
	
	echo rawdepth=========${dirList[i]}
	samtools depth ${dir}/${dirList[i]} > ${tempdir}/${dirList[i]}_fullinfodepth.txt
	awk '{print $3}' ${tempdir}/${dirList[i]}_fullinfodepth.txt > ${outdir}/${dirList[i]}_depth

	(( i++ ))
done



echo "now run_mean_sample_v3_full_aftermakedepth.sh ................. "

./run_mean_sample_v3_full_aftermakedepth.sh  ${outdir} ${prefix}


