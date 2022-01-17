infolder=$1



outfolder=${infolder}_thresholdpos

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 cpg_of_aCTwithspecific_threshold.py   ${infolder}/${dirList[i]} -0.7  ${outfolder}/${dirList[i]}

	python3 cpg_of_aCTwithspecific_threshold.py   ${infolder}/${dirList[i]} -0.8  ${outfolder}/${dirList[i]}

	python3 cpg_of_aCTwithspecific_threshold.py   ${infolder}/${dirList[i]} -0.9  ${outfolder}/${dirList[i]}

	(( i++ ))

done


