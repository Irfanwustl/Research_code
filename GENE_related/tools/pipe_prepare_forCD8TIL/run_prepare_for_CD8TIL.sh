infolder=$1



outfolder=${infolder}_onlyCD8TIL_meltumor

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 prepare_for_CD8TIL.py   ${infolder}/${dirList[i]} ${outfolder}/${dirList[i]}



	(( i++ ))

done


