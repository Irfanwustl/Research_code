


outfolder=$1


#######step2: generate all combinations of thresholdpos threshold  pos####


step2folder=${outfolder}_allthresholdcombinations

mkdir ${step2folder}


#######if I want to flexible number of stepsi.e. not just 3 compartments, only need to fix the following python code###############

python3 step2_allcombination_position_generalized.py ${outfolder} ${step2folder}



echo step2 done







