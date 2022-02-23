infolder=$1





outfolder=$2

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 adddumy_compartment_removeend_hardcoded.py   ${infolder}/${dirList[i]}    ${outfolder}/${dirList[i]}



	(( i++ ))

done


