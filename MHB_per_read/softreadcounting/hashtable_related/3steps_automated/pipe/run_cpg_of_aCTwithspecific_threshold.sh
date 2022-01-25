infile=$1

celltype=$2



outfolder=$3



inbase=$( basename ${infile} )






python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.05  ${outfolder}/${inbase}  ${celltype}


python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.1  ${outfolder}/${inbase}  ${celltype}



python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.2  ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.3 ${outfolder}/${inbase}  ${celltype}



python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.4  ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.5  ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.6 ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.7  ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.8  ${outfolder}/${inbase}  ${celltype}

python3 cpg_of_aCTwithspecific_threshold.py   ${infile} -0.9  ${outfolder}/${inbase}  ${celltype}






