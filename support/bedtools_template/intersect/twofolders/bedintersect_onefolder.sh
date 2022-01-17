fileA=$1
folderB=$2

outfolder=$3


dirList=($( ls ${folderB} ))

fileAbase=$( basename ${fileA} )



i=0
while (( i < ${#dirList[@]} ))
do



	bedtools intersect -a ${fileA} -b ${folderB}/${dirList[i]} -header -u > ${outfolder}/${fileAbase}_intwith_${dirList[i]}

	(( i++ ))

done




