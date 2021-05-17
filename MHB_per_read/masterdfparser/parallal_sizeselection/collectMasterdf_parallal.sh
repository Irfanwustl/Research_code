start=$SECONDS


alloutfolder=$1

mincpg=$2
maxcpg=$3

suffix=masterdf.txt #ABSreadcount_divisionedNormalized.txt

dirList=($( ls ${alloutfolder} ))






i=0
while (( i < ${#dirList[@]} ))
do
	temresultout=${alloutfolder}/${dirList[i]}/${dirList[i]}_${suffix}temp
	mkdir ${temresultout}
	cp ${alloutfolder}/${dirList[i]}/*${suffix} ${temresultout}




	masterdfinfolder=${temresultout}

	


	outdir=${masterdfinfolder}_finalized


	masterdirList=($( ls ${masterdfinfolder} ))


	mkdir ${outdir}


	masterdfinfoldermasterdirList=()
	tempdirnovlist=()
	jlist=()

	j=${mincpg}
	while (( j <= ${maxcpg} ))
	do

		tempdirnov=${outdir}/nocov_mincpg${j}
		mkdir ${tempdirnov}

		tempdirnovlist+=( ${tempdirnov} )
		jlist+=( ${j} )


		(( j++ ))
	done

	k=0
	while (( k < ${#masterdirList[@]} ))
	do
		masterdfinfoldermasterdirList+=( ${masterdfinfolder}/${masterdirList[k]} )

		  

		

		(( k++ ))

	done

	#echo ${masterdfinfoldermasterdirList[@]} 
	#echo ${tempdirnovlist[@]}
	#echo ${jlist[@]}


	parallel  -j 39 python3 adapterforparseMasterDF.py ::: ${masterdfinfoldermasterdirList[@]} ::: ${tempdirnovlist[@]} :::+ ${jlist[@]} ::: -99999 :::  nov 
	
	###./pipeadapterforMasterDF.sh ${temresultout} ${mincpg} ${maxcpg}



	(( i++ ))
done





end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

