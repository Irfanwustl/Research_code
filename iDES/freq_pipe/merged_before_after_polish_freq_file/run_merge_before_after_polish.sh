#! /bin/bash


beforedir=$1 ##### before_polish_freq_file_folder
afterdir=$2 ##### after_polish_freq_file_folder
outdir="${beforedir}_${afterdir}_merged"

mkdir  ${outdir}



dirList=($( ls ${beforedir} ))


i=0
while (( i < ${#dirList[@]} ))  ##means flist
do
	echo beforepolish=========${dirList[i]}
	bname=$(basename "${dirList[i]}" .txt)
	afterpolisfile=${bname}.rmbg.txt 
	echo afterpolis========${afterpolisfile}

	python3 merge_before_after_polished.py ${beforedir}/${dirList[i]} ${afterdir}/${afterpolisfile} ${outdir}/${afterpolisfile}_merged.txt

	(( i++ ))
done



