infolder=$1



outfolder=${infolder}_BL21

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 prepare_for_BL21.py   ${infolder}/${dirList[i]} ${outfolder}/${dirList[i]}



	(( i++ ))

done


