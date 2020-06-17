#! /bin/bash


dir=$1 ##### freq_file_folder
outdir="${dir}_bed"
mkdir  ${outdir}


dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do

	
	
	echo bed=========${dirList[i]}
	python3 freq2bedv2.py ${dir}/${dirList[i]}  ${outdir}/${dirList[i]}.bed

	(( i++ ))
done