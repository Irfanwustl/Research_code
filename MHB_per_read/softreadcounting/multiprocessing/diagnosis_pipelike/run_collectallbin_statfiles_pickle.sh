


globaloutfolder=$1

suffix=binnedstats.pkl


outfolder=${globaloutfolder}_${suffix}

dirList=($( ls ${globaloutfolder} | grep -h '\_result$' ))


mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	echo nowSM=========${dirList[i]} 


	python3 collectallbin_statfiles_pickle.py ${globaloutfolder}/${dirList[i]} ${outfolder}/${dirList[i]} ${suffix}


	(( i++ ))

done



