

geneFile=$1



allmatgeneFile=$2





outfolder=${allmatgeneFile}_${geneFile}


mkdir ${outfolder}




python3 group_based_on_feature.py  ${geneFile}  ${allmatgeneFile} ${outfolder}




