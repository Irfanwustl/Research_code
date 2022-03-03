
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

echo ${subdirs[@]} 
echo ${dirList[@]}

parallel  -j ${coretouse} ./juststep2.sh ::: ${subdirs[@]}  