

cram_in=$1

outdir=${cram_in}_bg

dirList=($( ls $cram_in ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo celltype=========${dirList[i]} 

	
	exlist=($( ls ${cram_in}/${dirList[i]} ))

	j=0
	while (( j < ${#exlist[@]} ))
	do
		echo ex=========${exlist[j]} 
		bwlist=($( ls ${cram_in}/${dirList[i]}/${exlist[j]} ))

		k=0
		while (( k < ${#bwlist[@]} ))
		do
			echo file=========${bwlist[k]}


			#./bigWigToBedGraph ${cram_in}/${dirList[i]}/${exlist[j]}/${bwlist[k]} ${outdir}/${bwlist[k]}.bedgraph  
			(( k++ ))
		done


		(( j++ ))
	done

	
 	(( i++ ))
done