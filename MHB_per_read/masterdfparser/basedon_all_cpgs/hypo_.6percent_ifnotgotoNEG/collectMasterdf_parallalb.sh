start=$SECONDS


alloutfolder=$1

mincpg=$2
maxcpg=$3

coretouse=$4

suffix=masterdf.txt #ABSreadcount_divisionedNormalized.txt

dirList=($( ls ${alloutfolder} ))




masterdfinfoldermasterdirList=()
tempdirnovlist=()
jlist=()


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

	k=0
	while (( k < ${#masterdirList[@]} ))
	do

		j=${mincpg}
		while (( j <= ${maxcpg} ))
		do
			masterdfinfoldermasterdirList+=( ${masterdfinfolder}/${masterdirList[k]} )
			
			tempdirnov=${outdir}/nocov_mincpg${j}
			
			if (( k == 0 ))
			then
				mkdir ${tempdirnov}
			fi

			tempdirnovlist+=( ${tempdirnov} )
			jlist+=( ${j} )

			(( j++ ))
		done

		  
		(( k++ ))

	done

	#echo ${masterdfinfoldermasterdirList[@]} 
	#echo ${tempdirnovlist[@]}
	#echo ${jlist[@]}

	
	###./pipeadapterforMasterDF.sh ${temresultout} ${mincpg} ${maxcpg}



	(( i++ ))
done

parallel  -j ${coretouse} python3 adapterforparseMasterDF.py ::: ${masterdfinfoldermasterdirList[@]} :::+ ${tempdirnovlist[@]} :::+ ${jlist[@]} ::: -99999 :::  nov


./collectResult_fromfinal.sh ${alloutfolder} ABSreadcount_divisioned.txt

./collectResult_fromfinal.sh ${alloutfolder} ABSreadcount_divisionedNormalized.txt


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

