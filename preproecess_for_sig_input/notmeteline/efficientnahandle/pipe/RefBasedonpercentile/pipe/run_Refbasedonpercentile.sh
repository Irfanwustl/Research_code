indir=$1 #/Users/irffanalahi/Research/Research_update/SM/melcfdref/Allseperated/differenttil/meldifferentTIL_genebody_input_out_mincpg2_q0.05_diff0.1_hypoTIL_genomic_feature_withrepeat_header_celltypeseperated/rowcombined_relevantgenes/Dashboard/bothdelta_q/towardsSM/alldmr

outdir=${indir}_refdmr

mkdir ${outdir}

dirList=($( ls ${indir} ))




i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 Refbasedondifferentpercentile.py ${indir}/${dirList[i]} ${outdir}/${dirList[i]} diff
	python3 Refbasedondifferentpercentile.py ${indir}/${dirList[i]} ${outdir}/${dirList[i]} maxCompartmentwisedelta
 	(( i++ ))
done
