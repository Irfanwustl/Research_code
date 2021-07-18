start=$SECONDS

infolder=$1
mincpg=2
outdir=${infolder}_out_mincpg${mincpg}

dirList=($( ls ${infolder}  ))

mkdir ${outdir}_raw
mkdir ${outdir}

declare -a inlist
declare -a outlist

i=0
while (( i < ${#dirList[@]} ))
do
    inlist+=(${infolder}/${dirList[i]})
    (( i++ ))
done

parallel --results ${outdir}_raw ./metilene -m ${mincpg} -c 2 -a g1 -b g2 ::: ${inlist[@]}

python3 copy_files.py ${outdir}_raw

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
