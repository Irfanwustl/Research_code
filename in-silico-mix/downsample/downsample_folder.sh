mergedfolder=$1
start=$2   
end=$3   #probably cannot input 100. but 99 is okay
gap=$4

outdir=${mergedfolder}_percentage_${start}_${end}_${gap}

mkdir ${outdir}


dirList=($( ls ${mergedfolder}  ))



i=0
while (( i < ${#dirList[@]} ))
do
	mkdir ${outdir}/${dirList[i]}


	current=${start}
	while [ ${current} -le ${end} ]
	do
		
		./downsample.sh ${mergedfolder}/${dirList[i]} ${outdir}/${dirList[i]}/${dirList[i]}_percent_${current}.bam  ${current}


		current=$(( current+${gap} ))

	done

 	(( i++ ))
done

