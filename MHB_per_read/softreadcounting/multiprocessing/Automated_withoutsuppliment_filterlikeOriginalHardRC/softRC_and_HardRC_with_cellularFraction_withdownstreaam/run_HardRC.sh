infolder=$1

outfolder=$2


sminfofile=$3

source ${sminfofile}


#outfolder=${infolder}_HardRC

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 HardRC_hardcoded.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}

	

	(( i++ ))

done


