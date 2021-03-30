### it collects file from nocov_mincpg3 like dir   


alloutfolder=$1

suffix=$2  #final.txt #ABSreadcount_divisionedNormalized.txt

ultimateOutput=$3 #${alloutfolder}_${suffix}

dirList=($( ls ${alloutfolder} ))




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

		





		

		cp ${lowerlowerdir}/*${suffix} ${ultimateOutput}







		(( j++ ))
	done

	(( i++ ))
done