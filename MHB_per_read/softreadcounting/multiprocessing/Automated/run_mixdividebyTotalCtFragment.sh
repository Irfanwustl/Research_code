infolder=$1 #####ctfragtotal folder 
CSxfolder=$2



outfolder=$3

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	currentCSXoutfile=($( ls ${CSxfolder}/${dirList[i]}*  ))

	
	

	j=0
	while (( j < ${#currentCSXoutfile[@]} ))
	do
		csxfile=$( basename ${currentCSXoutfile[j]} )

		
		
		python3 mixdividebyTotalCtFragment.py  ${infolder}/${dirList[i]} ${CSxfolder}/${csxfile} ${outfolder}/divbyCtFRAG_${csxfile} 
		(( j++ ))
	done
	

	

	
	

	

	

	(( i++ ))

done


