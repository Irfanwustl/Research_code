
indir=$1 #onefile dir like /Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/Analysis/codedevelop/corr/plot_atatimecode

outdir=${indir}_journalversion

mkdir ${outdir}

dirList=($( ls ${indir} ))




i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 corr_plots_journalversion.py ${indir}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done




