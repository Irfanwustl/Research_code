
CSxfolder=$1

SMfolder=$2


outfolder=$3



mkdir ${outfolder}




smlist=($( ls ${SMfolder} ))
csxfollst=()
outfollst=()
smfollst=()


k=0
while (( k < ${#smlist[@]} ))

do 
	currentSM=${SMfolder}/${smlist[k]}








	currentCSXoutfile=($( ls ${CSxfolder}/${smlist[k]}*  ))

	
	

	j=0
	while (( j < ${#currentCSXoutfile[@]} ))
	do
		csxfile=$( basename ${currentCSXoutfile[j]} )
        csxfollst+=( ${CSxfolder}/${csxfile} )
        outfollst+=( ${outfolder}/method1Fract_${csxfile} )
        smfollst+=( ${SMfolder}/${smlist[k]} )
		
		
#		python3 ct_proportion_idea1.py   ${CSxfolder}/${csxfile} ${outfolder}/method1Fract_${csxfile}  ${SMfolder}/${smlist[k]}
		(( j++ ))
	done

		


	(( k++ ))

done

parallel python3 ct_proportion_idea1.py ::: ${csxfollst[@]} :::+ ${outfollst[@]} :::+ ${smfollst[@]} 
