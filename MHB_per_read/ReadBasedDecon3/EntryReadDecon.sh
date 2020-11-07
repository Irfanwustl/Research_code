


smfolder=$1 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/allSM

bamfolder=$2 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/bamfiles_onlyregionIN_smbluwgbsg50_hypo_radius_150bpSorted_600mergeddoublemerged_sorted






dirList=($( ls ${smfolder} ))

outfolder=${smfolder}_globalout
mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	echo nowSM=========${dirList[i]} 

	./runcommandline.sh ${smfolder}/${dirList[i]} ${bamfolder} ${outfolder}


	(( i++ ))

done


