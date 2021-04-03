start=$SECONDS



infolder=$1   #/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/Automate_afterrd/mergedifferent_output/corefromserverfolder


outdir=${infolder}_merged


dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do
	dummy=($( ls ${infolder}/${dirList[i]} ))
	

	filelist=($( ls ${infolder}/${dirList[i]}/${dummy[0]}  ))

	j=0
	while (( j < ${#filelist[@]} ))
	do

		python3 sendtospecificdir.py ${infolder}/${dirList[i]}/${dummy[0]}/${filelist[j]} ${outdir}    ### should be only one finalizedout like folder

		(( j++ ))
	done
	
 	(( i++ ))
done




./run_mergealldfinafolderrbindlike.sh ${outdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

