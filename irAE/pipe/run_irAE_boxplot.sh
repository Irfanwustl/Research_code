indir=$1 #onefile dir like /Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/Analysis/codedevelop/corr/plot_atatimecode

dirList=($( ls ${indir} ))




i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 irAE_boxplot.py ${indir}/${dirList[i]} 
 	(( i++ ))
done