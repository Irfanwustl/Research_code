infolder=$1
outdir=${infolder}_mapped 

dirList=($( ls ${infolder}  ))

mkdir ${outdir}




i=0
while (( i < ${#dirList[@]} ))
do
	
	

	inneroutdir=${outdir}/${dirList[i]}

	mkdir ${inneroutdir}

	
	./extractmappedreads.sh ${infolder}/${dirList[i]} ${inneroutdir}

	
 	(( i++ ))
done