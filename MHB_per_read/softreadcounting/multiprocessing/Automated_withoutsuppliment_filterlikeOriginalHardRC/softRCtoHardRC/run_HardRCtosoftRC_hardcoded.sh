infolder=$1



outfolder=${infolder}_HardRCtoSoftRC

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 HardRCtosoftRC_hardcoded.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]}

	

	(( i++ ))

done



onlyCSXoutfolder=${outfolder}_only_CSxOut

mkdir ${onlyCSXoutfolder}


cp ${outfolder}/*CSxOut.txt ${onlyCSXoutfolder}/

