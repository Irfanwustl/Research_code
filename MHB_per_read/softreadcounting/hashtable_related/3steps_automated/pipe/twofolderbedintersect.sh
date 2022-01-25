folderA=$1
folderB=$2
outfolder=$3

dirList=($( ls ${folderA} ))






mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	./bedintersect_onefolder.sh ${folderA}/${dirList[i]} ${folderB} ${outfolder}

	(( i++ ))

done


