infolder=$1 #####pkl final folder
CSxfolder=$2

SMfolder=$3


outfolder=$4


sminfofile=$5

source ${sminfofile}



mkdir ${outfolder}




smlist=($( ls ${SMfolder} ))


k=0
while (( k < ${#smlist[@]} ))

do 
	currentSM=${SMfolder}/${smlist[k]}




	currentFINALbinfilelist=($( ls ${infolder}/${smlist[k]}*  ))

	#####chek that there is only one And select that one

	lengthofbinfiles=${#currentFINALbinfilelist[@]}

	if [ ${lengthofbinfiles} -ne 1 ]
	then
		echo problem in masscore idea running
		exit
	fi

	currentFINALbinfile=${currentFINALbinfilelist[0]}

	currentFINALbinfile=$( basename ${currentFINALbinfile} )


	tomatchwithCSX=${currentFINALbinfile%_FINAL_binnedstats.pkl}



	currentCSXoutfile=($( ls ${CSxfolder}/${tomatchwithCSX}*  ))

	
	

	j=0
	while (( j < ${#currentCSXoutfile[@]} ))
	do
		csxfile=$( basename ${currentCSXoutfile[j]} )

		
		
		python3 softRC_theoritical_HARDCODED_but_DIFFERENT.py  ${infolder}/${currentFINALbinfile} ${CSxfolder}/${csxfile}  ${SMfolder}/${smlist[k]}   ${outfolder}/maxscorFract_${csxfile} ${smsoftRC_theoritical_HARDCODED[@]}
		(( j++ ))
	done

		


	(( k++ ))

done

