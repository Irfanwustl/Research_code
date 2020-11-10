


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


