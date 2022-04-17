infolder=$1

outfolder=$2


sminfofile=$3

source ${sminfofile}


#outfolder=${infolder}_HardRC

mkdir ${outfolder}

dirList=($( ls ${infolder} ))

infollst=()
outfollst=()


i=0
while (( i < ${#dirList[@]} ))
do

    
    infollst+=( ${infolder}/${dirList[i]} )
    outfollst+=( ${outfolder}/${dirList[i]} )
#    python3 HardRC_hardcoded.py  ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}
#    echo ${infolder}/${dirList[i]}  ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}
    

    (( i++ ))

done

hardcodedlst=${allhardcodedfile[@]}

parallel --env hardcodedlst python3 HardRC_hardcoded.py {=uq=} ::: ${infollst[@]} :::+ ${outfollst[@]} ::: "$hardcodedlst"
