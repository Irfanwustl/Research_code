start=$SECONDS


masterdfinfolder=$1

mincpg=$2
maxcpg=$3


cpgcova=1
cpgcovb=-1
cpgcovc=-2
cpgcovd=-3
cpgcove=0.5

outdir=${masterdfinfolder}_finalized


dirList=($( ls ${masterdfinfolder} ))


mkdir ${outdir}



j=${mincpg}
while (( j <= ${maxcpg} ))
do

	tempdirnov=${outdir}/nocov_mincpg${j}
	mkdir ${tempdirnov}

	



	i=0
	while (( i < ${#dirList[@]} ))
	do

		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdirnov}  -99999  ${j}  nov   

		

		(( i++ ))

	done


	(( j++ ))
done


wait


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

