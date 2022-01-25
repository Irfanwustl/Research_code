infile=$1

celltype=$2



outfolder=$3



inbase=$( basename ${infile} )






python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.5  ${outfolder}/${inbase}  ${celltype}


python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.1  ${outfolder}/${inbase}  ${celltype}





