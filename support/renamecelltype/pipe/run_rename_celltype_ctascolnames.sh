infolder=$1



outfolder=${infolder}_ctRenamed

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 rename_celltype_ctascolnames.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]}

	

	(( i++ ))

done


