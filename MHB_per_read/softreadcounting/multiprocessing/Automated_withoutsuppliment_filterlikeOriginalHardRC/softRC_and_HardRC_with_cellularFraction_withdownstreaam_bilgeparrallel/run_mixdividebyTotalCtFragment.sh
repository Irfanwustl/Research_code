infolder=$1 #####ctfragtotal folder 
CSxfolder=$2



outfolder=$3

mkdir ${outfolder}

dirList=($( ls ${infolder} ))
infollst=()
csxfollst=()
outfollst=()


i=0
while (( i < ${#dirList[@]} ))
do

    currentCSXoutfile=($( ls ${CSxfolder}/${dirList[i]}*  ))
    
    

    j=0
    while (( j < ${#currentCSXoutfile[@]} ))
    do
        csxfile=$( basename ${currentCSXoutfile[j]} )
        infollst+=( ${infolder}/${dirList[i]} )
        csxfollst+=( ${CSxfolder}/${csxfile} )
        #outfollst+=( ${outfolder}/divbyCtFRAG_${csxfile} )
        
#        python3 mixdividebyTotalCtFragment.py  ${infolder}/${dirList[i]} ${CSxfolder}/${csxfile} ${outfolder}/divbyCtFRAG_${csxfile}
        (( j++ ))
    done
    
    (( i++ ))

done

outfol=${outfolder}/divbyCtFRAG_${csxfile}

parallel python3 mixdividebyTotalCtFragment.py ::: ${infollst[@]} :::+ ${csxfollst[@]} ::: ${outfol}
