
CSxfolder=$1

SMfolder=$2


outfolder=$3



mkdir ${outfolder}




smlist=($( ls ${SMfolder} ))


k=0
while (( k < ${#smlist[@]} ))

do 
	currentSM=${SMfolder}/${smlist[k]}








	currentCSXoutfile=($( ls ${CSxfolder}/${smlist[k]}*  ))

	
	

	j=0
	while (( j < ${#currentCSXoutfile[@]} ))
	do
		csxfile=$( basename ${currentCSXoutfile[j]} )

		
		
		python3 ct_proportion_idea1.py   ${CSxfolder}/${csxfile} ${outfolder}/method1Fract_${csxfile}  ${SMfolder}/${smlist[k]}   
		(( j++ ))
	done

		


	(( k++ ))

done

