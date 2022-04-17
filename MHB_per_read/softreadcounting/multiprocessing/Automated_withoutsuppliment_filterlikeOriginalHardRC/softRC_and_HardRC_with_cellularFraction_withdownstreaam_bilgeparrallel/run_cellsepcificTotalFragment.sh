infolder=$1



outfolder=$2


sminfofile=$3

source ${sminfofile}

mkdir ${outfolder}

dirList=($( ls ${infolder} ))
infolderlst=()
outfolderlst=()

i=0
while (( i < ${#dirList[@]} ))
do

#    python3 cellsepcificTotalFragment_HARDCODED.py   ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}
    infolderlst+=( ${infolder}/${dirList[i]} )
    outfolderlst+=( ${outfolder}/${dirList[i]} )
    

    (( i++ ))

done

hardcodedlst=${allhardcodedfile[@]}

parallel --env hardcodedlst python3 cellsepcificTotalFragment_HARDCODED.py {=uq=} ::: ${infolderlst[@]} :::+ ${outfolderlst[@]} ::: "$hardcodedlst"

