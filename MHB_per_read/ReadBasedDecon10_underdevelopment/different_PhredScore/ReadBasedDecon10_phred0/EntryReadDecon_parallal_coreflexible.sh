
start=$SECONDS


smfolder=$1 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/allSM

bamfolder=$2 #/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/pipe_codevelop2/bamfiles_onlyregionIN_smbluwgbsg50_hypo_radius_150bpSorted_600mergeddoublemerged_sorted

coretouse=$3




dirList=($( ls ${smfolder} ))

bambase=$( basename ${bamfolder} )

outfolder=${smfolder}_${bambase}_globalout
mkdir ${outfolder}

smlist=()
infilelist=()
outfilelist=()

i=0
while (( i < ${#dirList[@]} ))
do

	sm=${dirList[i]}
	globalout=${outfolder}


	


	smbasename=$( basename ${sm} )

	smoutfolder=${globalout}/${smbasename}_result


	mkdir ${smoutfolder}


	


	bamdirList=($( ls ${bamfolder} | grep -v '\.bai$'))



	j=0
	while (( j < ${#bamdirList[@]} ))
	do

		smlist+=( ${smfolder}/${dirList[i]} )

		infilelist+=( ${bamfolder}/${bamdirList[j]} )

		outfilelist+=( ${smoutfolder}/${bamdirList[j]} ) 

		

		


		(( j++ ))

	done

	


	(( i++ ))

done


echo ${#smlist[@]}
echo ${#infilelist[@]}
echo ${#outfilelist[@]}


parallel  -j ${coretouse} python3 runcommandline.py ::: ${smlist[@]} :::+ ${infilelist[@]} :::+ ${outfilelist[@]} 


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

