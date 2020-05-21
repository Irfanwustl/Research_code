#! /bin/bash


dir=$1 ##### nohlca_bed file folder 
outdir="${dir}_bg"
mkdir  ${outdir}

dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do

	
	
	echo bed=========${dirList[i]}
	cut -f 1-4 ${dir}/${dirList[i]} > ${outdir}/${dirList[i]}.bedgraph

	(( i++ ))
done