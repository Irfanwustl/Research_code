


masterdfinfolder=$1

mincpg=$2
maxcpg=$3


cpgcova=0
cpgcovb=1

outdir=${masterdfinfolder}_finalized


dirList=($( ls ${masterdfinfolder} ))


mkdir ${outdir}



j=${mincpg}
while (( j <= ${maxcpg} ))
do


	tempdira=${outdir}/cov${cpgcova}_mincpg${j}
	mkdir ${tempdira}
	tempdirb=${outdir}/cov${cpgcovb}_mincpg${j}
	mkdir ${tempdirb}



	i=0
	while (( i < ${#dirList[@]} ))
	do

	
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdira}  ${cpgcova}  ${j}
		python3 adapterforparseMasterDF.py ${masterdfinfolder}/${dirList[i]} ${tempdirb}  ${cpgcovb}  ${j}

		(( i++ ))

	done


	(( j++ ))
done


