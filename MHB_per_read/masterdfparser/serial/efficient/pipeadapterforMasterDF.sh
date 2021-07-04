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

	tempdira=${outdir}/cov${cpgcova}_mincpg${j}
	mkdir ${tempdira}
	tempdirb=${outdir}/cov${cpgcovb}_mincpg${j}
	mkdir ${tempdirb}
	tempdirc=${outdir}/cov${cpgcovc}_mincpg${j}
	mkdir ${tempdirc}
	tempdird=${outdir}/cov${cpgcovd}_mincpg${j}
	mkdir ${tempdird}
	tempdire=${outdir}/cov${cpgcove}_mincpg${j}
	mkdir ${tempdire}



	i=0
	while (( i < ${#dirList[@]} ))
	do

		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdirnov}  -99999  ${j}  nov   &

		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdira}  ${cpgcova}  ${j}  ov   &
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdirb}  ${cpgcovb}  ${j}  ov   &
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdirc}  ${cpgcovc}  ${j}  ov   &
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdird}  ${cpgcovd}  ${j}  ov   &
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdire}  ${cpgcove}  ${j}  ov   &

		(( i++ ))

	done


	(( j++ ))
done


wait


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

