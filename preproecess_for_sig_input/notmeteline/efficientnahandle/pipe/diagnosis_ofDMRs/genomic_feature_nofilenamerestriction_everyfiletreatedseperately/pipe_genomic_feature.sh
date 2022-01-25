start=$SECONDS

headerlessmetoutfolder=$1
genomicfeaturefolder=$2



genomicfeaturefolderbase=$( basename ${genomicfeaturefolder} )



outdir=${headerlessmetoutfolder}_${genomicfeaturefolderbase}


dirList=($( ls ${genomicfeaturefolder}  ))





mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do
	
	./bedintersect_genome.sh ${headerlessmetoutfolder}  ${genomicfeaturefolder}/${dirList[i]}  ${outdir}

	(( i++ ))
done




##### pending: add not found part



headeradded=${outdir}_header

./run_addheader_withgenomefeature.sh ${outdir} ${headeradded}


celltypeseperated=${headeradded}_celltypeseperated

./run_mycopy.sh ${headeradded} ${celltypeseperated} ${genomicfeaturefolder}

./run_mergealldfinafolderrbindlike.sh ${celltypeseperated}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
