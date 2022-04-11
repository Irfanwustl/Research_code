infolder=$1



outfolder=$2      #{infolder}_HardRCtoSoftRC

sminfofile=$3

source ${sminfofile}

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 HardRCtosoftRC_hardcoded.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}

	

	(( i++ ))

done



onlyCSXoutfolder=${outfolder}_only_CSxOut

mkdir ${onlyCSXoutfolder}


cp ${outfolder}/*CSxOut.txt ${onlyCSXoutfolder}/

