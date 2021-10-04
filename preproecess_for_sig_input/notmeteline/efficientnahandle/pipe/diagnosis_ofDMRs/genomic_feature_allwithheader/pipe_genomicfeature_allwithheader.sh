start=$SECONDS

metoutfolder=$1  #### must have header
genomicfeaturefolder=$2  #### must have header


genomicfeaturefolderbase=$( basename ${genomicfeaturefolder} )


outdir=${metoutfolder}_${genomicfeaturefolderbase}


dirList=($( ls ${genomicfeaturefolder}  ))

mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do
	
	./bedintersect_genome_handle_header.sh ${metoutfolder}  ${genomicfeaturefolder}/${dirList[i]}  ${outdir}

	(( i++ ))
done



celltypeseperated=${outdir}_celltypeseperated

./run_mycopy.sh ${outdir} ${celltypeseperated}




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


