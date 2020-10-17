
start=$SECONDS

fileqithblockinfoFolder=$1


startcpgCount=$2

endcpgCount=$3

outdir=${fileqithblockinfoFolder}_Ready

mkdir ${outdir}

dirList=($( ls ${fileqithblockinfoFolder} ))


i=0
while (( i < ${#dirList[@]} ))
do


	j=${startcpgCount}
	while (( j <= ${endcpgCount} ))
	do
		filepath=${fileqithblockinfoFolder}/${dirList[i]}
		
		fname=$( basename ${filepath} )

		python3 dropunique.py ${filepath}  ${j} ${outdir}/${fname}_${j}cpg &

		(( j++ ))
	done




	(( i++ ))
done



wait

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



