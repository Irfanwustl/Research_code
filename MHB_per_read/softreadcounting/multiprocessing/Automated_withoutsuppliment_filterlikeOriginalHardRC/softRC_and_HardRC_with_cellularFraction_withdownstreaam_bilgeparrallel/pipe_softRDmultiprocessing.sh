





bamfolder=$1
smfile=$2

globalout=$3

coretouse=$4

smbasename=$( basename ${smfile} )




outdir=${globalout}/${smbasename}_result

dirList=($( ls ${bamfolder} | grep -v '\.bai$'))

bamfollist=()

mkdir ${outdir}

outdirlist=()

smfilelst=()

i=0
while (( i < ${#dirList[@]} ))
do

    #echo now=========${dirList[i]}
    

#    python3 softRDmultiprocessing.py ${bamfolder}/${dirList[i]} ${smfile}  ${outdir}/${dirList[i]} ${coretouse}
    outdirlist+=( ${outdir}/${dirList[i]} )
    bamfollist+=( ${bamfolder}/${dirList[i]} )
    smfilelst+=( ${smfile} )
    (( i++ ))
done

parallel -j ${coretouse} python3 softRDmultiprocessing.py ::: ${bamfollist[@]} :::+ ${smfilelst[@]} :::+ ${outdirlist[@]} ::: ${coretouse}


python3 combineresult_formergingwithgt.py ${outdir}
