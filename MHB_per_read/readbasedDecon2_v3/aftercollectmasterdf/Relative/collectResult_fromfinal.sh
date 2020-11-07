
alloutfolder=$1

suffix=ABSreadcount_divisionedNormalized.txt

dirList=($( ls ${alloutfolder} ))


ultimateOutput=${alloutfolder}_finalizedOut

mkdir ${ultimateOutput}



i=0
while (( i < ${#dirList[@]} ))
do
	lowerdir=${alloutfolder}/${dirList[i]}/${dirList[i]}_masterdf.txttemp_finalized

	lowerdirlist=($( ls ${lowerdir} ))

	j=0
	while (( j < ${#lowerdirlist[@]} ))
	do
		lowerlowerdir=${lowerdir}/${lowerdirlist[j]}

		

		temresultout=${lowerlowerdir}/${dirList[i]}_${lowerdirlist[j]}_${suffix}_CSxOut

		mkdir ${temresultout}



		

		cp ${lowerlowerdir}/*${suffix} ${temresultout}

		python3 store_the_results.py ${temresultout} ${temresultout}.txt

		cp ${temresultout}.txt ${ultimateOutput}





		(( j++ ))
	done

	(( i++ ))
done