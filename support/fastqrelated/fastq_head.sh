start=$SECONDS

infolder=$1
readnum=$2  #multiple of 4



outdir=${infolder}_headnotread${readnum}

dirList=($( ls ${infolder}/*fastq.gz  ))


mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo ${dirList[i]}

	outname=$( basename ${dirList[i]%.gz} )

	
	zcat ${dirList[i]} | head -n ${readnum} > ${outdir}/${outname}
	

	gzip ${outdir}/${outname}

	(( i++ ))
done


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"