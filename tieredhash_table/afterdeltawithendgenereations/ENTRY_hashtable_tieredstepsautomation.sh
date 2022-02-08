

deltaWithEndfolder=$1

celltype=$2 #CD8TIL

dirList=($( ls ${deltaWithEndfolder} ))


#######step1: get compartmentwise threshold  pos####

outfolder=${deltaWithEndfolder}_thresholdpos

mkdir ${outfolder}

i=0
while (( i < ${#dirList[@]} ))
do

	

	
	tempout=${outfolder}/${dirList[i]}_thresholdpos

	mkdir  ${tempout}

	./run_cpg_of_aCTwithspecific_threshold.sh  ${deltaWithEndfolder}/${dirList[i]}   ${celltype} ${tempout}

	

	

	(( i++ ))

done

echo step1 done

#######step2: generate all combinations of thresholdpos threshold  pos####


step2folder=${outfolder}_allthresholdcombinations

mkdir ${step2folder}


#######if I want to flexible number of stepsi.e. not just 3 compartments, only need to fix the following python code###############

python3 step2_allcombination_position_generalized.py ${outfolder} ${step2folder}



echo step2 done

###########step3: intersect delta folder with all combinaions####

step2folderBbase=$( basename ${step2folder} )

step3folder=${deltaWithEndfolder}_int_${step2folderBbase}

./twofolderbedintersect.sh ${deltaWithEndfolder} ${step2folder}  ${step3folder}


echo step3 done

###########step4: final sm #########

############### Need  to write ##################################





