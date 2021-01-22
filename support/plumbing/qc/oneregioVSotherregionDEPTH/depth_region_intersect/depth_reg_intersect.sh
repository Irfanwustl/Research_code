start=$SECONDS


infolder=$1
regfile=$2  ###noheader


regfilename=$( basename ${regfile} )
outdir=${infolder}_intwith_${regfilename}


dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	
	bedtools intersect -a ${infolder}/${dirList[i]} -b ${regfile} -wa -wb  > ${outdir}/${dirList[i]}_${regfilename}_depth.txt &
 	(( i++ ))
done

wait

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
