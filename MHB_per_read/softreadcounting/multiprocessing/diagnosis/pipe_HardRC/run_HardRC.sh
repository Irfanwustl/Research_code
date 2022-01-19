infolder=$1



outfolder=${infolder}_HardRC

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 HardRC.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]}

	

	(( i++ ))

done


