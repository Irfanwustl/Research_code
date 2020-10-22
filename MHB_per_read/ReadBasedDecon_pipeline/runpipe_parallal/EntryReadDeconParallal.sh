
start=$SECONDS




smfolder=$1 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/allSM

bamfolder=$2 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/bamfiles_onlyregionIN_smbluwgbsg50_hypo_radius_150bpSorted_600mergeddoublemerged_sorted






dirList=($( ls ${smfolder} ))


bamdirList=($( ls ${bamfolder} | grep -v '\.bai$'))

outfolder=${smfolder}_globalout
mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	
	


	currentsm=${smfolder}/${dirList[i]}

	smbasename=$( basename ${currentsm} )

	smoutfolder=${outfolder}/${smbasename}_result


	mkdir ${smoutfolder}

	j=0
	while (( j < ${#bamdirList[@]} ))
	do
		python3 runcommandline.py ${currentsm} ${bamfolder}/${bamdirList[j]}  ${smoutfolder}/${bamdirList[j]}  &

		(( j++ ))

	done



	(( i++ ))

done


wait


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"




