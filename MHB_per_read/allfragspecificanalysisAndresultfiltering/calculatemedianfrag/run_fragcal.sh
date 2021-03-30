alloutfolder=$1



dirList=($( ls ${alloutfolder} ))



i=0
while (( i < ${#dirList[@]} ))
do
	lowerdir=${alloutfolder}/${dirList[i]}/${dirList[i]}_masterdf.txttemp_finalized

	lowerdirlist=($( ls ${lowerdir} ))

	j=0
	while (( j < ${#lowerdirlist[@]} ))
	do
		lowerlowerdir=${lowerdir}/${lowerdirlist[j]}


		finalfiles=($( ls ${lowerlowerdir}/*final.txt )) #/*.final.txt

		k=0
		while (( k < ${#finalfiles[@]} ))
		do
			python3 fragcal.py ${finalfiles[k]} ${finalfiles[k]}_fraginfo.txt

			(( k++ ))
		done

		(( j++ ))
	done

	(( i++ ))
done
