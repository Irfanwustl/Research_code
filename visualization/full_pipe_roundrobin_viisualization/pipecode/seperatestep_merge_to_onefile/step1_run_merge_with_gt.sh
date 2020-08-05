


csxoutfolder=$1
gtfolder=$2

mergedfolder=$3

mkdir ${mergedfolder}


csxList=($( ls ${csxoutfolder} ))


gtlist=($( ls ${gtfolder} ))


i=0
while (( i < ${#csxList[@]} ))
do

	mkdir ${mergedfolder}/${csxList[i]}
	j=0
	while (( j < ${#gtlist[@]} ))
	do


		
		Rscript merge_with_gt.R ${csxoutfolder}/${csxList[i]}  ${gtfolder}/${gtlist[j]} ${mergedfolder}/${csxList[i]}/${csxList[i]}_${gtlist[j]}

		(( j++ ))
	done

	(( i++ ))
done




