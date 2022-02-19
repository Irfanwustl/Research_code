infol=$1

coretouse=$2


dirList=($( ls ${infol} ))

subdirs=()

#celltypes=(MEL_TUMOR PBL CD8TIL)

i=0
while (( i < ${#dirList[@]} ))
do

	subdirs+=( ${infol}/${dirList[i]} )

	(( i++ ))

done




parallel  -j ${coretouse} python3 subset_files.py ::: ${subdirs[@]} 

