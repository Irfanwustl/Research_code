#! /bin/bash


dir=$1 ##### raw bed file folder from biscuit
outdir="${dir}_nohla"
mkdir  ${outdir}


dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do

	
	
	echo rawbed=========${dirList[i]}
	sed '/HLA/d' ${dir}/${dirList[i]} > ${outdir}/${dirList[i]}

	(( i++ ))
done