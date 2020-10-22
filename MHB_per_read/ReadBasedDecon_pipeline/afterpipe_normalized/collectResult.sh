


alloutfolder=$1

suffix=ABSreadcount_divisionedNormalized.txt

dirList=($( ls ${alloutfolder} ))


ultimateOutput=${alloutfolder}_organizedOut

mkdir ${ultimateOutput}



i=0
while (( i < ${#dirList[@]} ))
do
	temresultout=${alloutfolder}/${dirList[i]}/${dirList[i]}_${suffix}_CSxOut
	mkdir ${temresultout}
	cp ${alloutfolder}/${dirList[i]}/*${suffix} ${temresultout}

	python3 store_the_results.py ${temresultout} ${temresultout}.txt

	cp ${temresultout}.txt ${ultimateOutput}

	(( i++ ))
done


