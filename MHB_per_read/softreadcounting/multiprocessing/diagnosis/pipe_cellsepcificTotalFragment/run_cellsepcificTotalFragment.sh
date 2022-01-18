infolder=$1



outfolder=${infolder}_ctTotalFrag

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 cellsepcificTotalFragment.py   ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]}

	

	(( i++ ))

done


