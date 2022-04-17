


binnedfolder=$1

outfolder=$2

sminfofile=$3

source ${sminfofile}

mkdir ${outfolder}


dirList=($( ls ${binnedfolder} | grep -h '\_dupindex_binnedstats.pkl$' ))
binnedfolderlst=()
outfolderlst=()



i=0
while (( i < ${#dirList[@]} ))
do

    #echo now=========${dirList[i]}

#    python3 score_flexible_HARDCODED.py ${binnedfolder}/${dirList[i]}   ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}
    binnedfolderlst+=( ${binnedfolder}/${dirList[i]} )
    outfolderlst+=( ${outfolder}/${dirList[i]} )
    (( i++ ))

done

hardcodedlst=${allhardcodedfile[@]}

parallel --env hardcodedlst python3 score_flexible_HARDCODED.py {=uq=} ::: ${binnedfolderlst[@]} :::+ ${outfolderlst[@]} ::: "$hardcodedlst"



