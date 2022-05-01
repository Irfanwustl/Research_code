#! /bin/bash

outdir=$1 #model_data_bam #YALE_model_data_bam











flag_outdir="${outdir}_flag"

mkdir ${flag_outdir}

f3List=($( ls ${outdir} ))

i=0

while (( i < ${#f3List[@]} ))
do

	echo flag=========${f3List[i]} 
	samtools flagstat ${outdir}/${f3List[i]} >    ${flag_outdir}/${f3List[i]}_flag

	(( i++ ))
done












