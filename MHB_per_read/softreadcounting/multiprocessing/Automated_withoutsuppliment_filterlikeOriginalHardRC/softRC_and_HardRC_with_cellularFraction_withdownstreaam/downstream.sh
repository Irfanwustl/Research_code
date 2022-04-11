


csxoutfolder=$1
gtfolder=$2
mergedfolder=$3

coretouse=$4



mkdir ${mergedfolder}

figdir=${mergedfolder}_figs
mkdir ${figdir}


csxList=($( ls ${csxoutfolder} ))


gtlist=($( ls ${gtfolder} ))

csxoutfolderlist=()
gtfolderlist=()
mergedfolderlst=()
figdirlist=()

i=0
while (( i < ${#csxList[@]} ))
do

	j=0
	while (( j < ${#gtlist[@]} ))
	do
        csxoutfolderlist+=( ${csxoutfolder}/${csxList[i]} )
        gtfolderlist+=( ${gtfolder}/${gtlist[j]} )
        mergedfolderlst+=( ${mergedfolder}/${csxList[i]}_${gtlist[j]} )
        figdirlist+=( ${figdir}/${csxList[i]}_${gtlist[j]} )
#		Rscript merge_with_gt.R ${csxoutfolder}/${csxList[i]} ${gtfolder}/${gtlist[j]} ${mergedfolder}/${csxList[i]}_${gtlist[j]}

#		python3 -W ignore corr_plots_journalversion.py ${mergedfolder}/${csxList[i]}_${gtlist[j]} ${figdir}/${csxList[i]}_${gtlist[j]}

#		python3 -W ignore cell_correlation_irf.py ${mergedfolder}/${csxList[i]}_${gtlist[j]} ${figdir}/${csxList[i]}_${gtlist[j]}

			

		(( j++ ))
	done

	(( i++ ))
done

parallel -j ${coretouse} Rscript merge_with_gt.R ::: ${csxoutfolderlist[@]} :::+ ${gtfolderlist[@]} :::+ ${mergedfolderlst[@]}

parallel -j ${coretouse} python3 -W ignore  corr_plots_journalversion.py ::: ${mergedfolderlst[@]} :::+ ${figdirlist[@]}

parallel -j ${coretouse} python3 -W ignore  cell_correlation_irf.py ::: ${mergedfolderlst[@]} :::+ ${figdirlist[@]}



