infolder=$1



outfolder=$2


sminfofile=$3

source ${sminfofile}

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 cellsepcificTotalFragment_HARDCODED.py   ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}

	

	(( i++ ))

done


