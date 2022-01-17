folderA=$1
folderB=$2

dirList=($( ls ${folderA} ))

folderBbase=$( basename ${folderB} )



outfolder=${folderA}_intwih_${folderBbase}
mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	./bedintersect_onefolder.sh ${folderA}/${dirList[i]} ${folderB} ${outfolder}

	(( i++ ))

done


