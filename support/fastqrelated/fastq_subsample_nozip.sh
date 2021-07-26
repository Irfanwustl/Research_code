start=$SECONDS

infolder=$1
readnum=$2

seedval=10

outdir=${infolder}_s${seedval}_readnum${readnum}

dirList=($( ls ${infolder}/*fastq.gz  ))


mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo ${dirList[i]}

	outname=$( basename ${dirList[i]} )

	

	seqtk sample -s ${seedval}  ${dirList[i]} ${readnum} > ${outdir}/${outname}

	#gzip ${outdir}/${outname}

	(( i++ ))
done


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"