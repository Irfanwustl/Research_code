infolder=$1
outdir=${infolder}_mdadded

dirList=($( ls ${infolder}  ))

mkdir ${outdir}




i=0
while (( i < ${#dirList[@]} ))
do
	
	

	inneroutdir=${outdir}/${dirList[i]}

	mkdir ${inneroutdir}

	
	./clmdinsilico.sh ${infolder}/${dirList[i]} ${inneroutdir}

	
 	(( i++ ))
done
