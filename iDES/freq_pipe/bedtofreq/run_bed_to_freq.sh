#! /bin/bash


dir=$1 ##### bed _file_folder_nohla 
outdir="${dir}_freq"
mkdir  ${outdir}


dirList=($( ls $dir ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do

	
	
	echo bed=========${dirList[i]}
	python3 bed2freq.py ${dir}/${dirList[i]}  ${outdir}/${dirList[i]}_freq.txt

	(( i++ ))
done