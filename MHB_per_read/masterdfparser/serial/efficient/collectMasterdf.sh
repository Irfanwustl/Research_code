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


	
	
	./pipeadapterforMasterDF.sh ${temresultout} ${mincpg} ${maxcpg}



	(( i++ ))
done



./collectResult_fromfinal.sh ${alloutfolder} ABSreadcount_divisioned.txt

./collectResult_fromfinal.sh ${alloutfolder} ABSreadcount_divisionedNormalized.txt




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

