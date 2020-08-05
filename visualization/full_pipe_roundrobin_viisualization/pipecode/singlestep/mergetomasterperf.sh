


csxoutfolder=$1
gtfolder=$2

mergedfolder=$3

masterfilename=$4  ### should be in the parent of csxoutfolder and gtfolder

puregtfilename=blueprint_rein_our_pbmc_puregt.txt

suffixonefile=onefile

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

		python3 mergegt_in_onefile.py ${mergedfolder}/${csxList[i]}/${csxList[i]}_${gtlist[j]} ${mergedfolder}/${csxList[i]}/${csxList[i]}_${gtlist[j]}_${suffixonefile}

		python3 recordroundrobin.py ${mergedfolder}/${csxList[i]}/${csxList[i]}_${gtlist[j]}_${suffixonefile} ${gtfolder} ${gtlist[j]}  ${puregtfilename}  ${masterfilename}

		(( j++ ))
	done

	(( i++ ))
done




