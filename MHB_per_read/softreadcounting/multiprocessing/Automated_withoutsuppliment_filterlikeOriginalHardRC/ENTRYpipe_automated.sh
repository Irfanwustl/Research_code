
start=$SECONDS


smfolder=$1 

bamfolder=$2 

coretouse=$3






dirList=($( ls ${smfolder} ))

bambase=$( basename ${bamfolder} )

outfolder=${smfolder}_${bambase}_globalout
mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	
	#echo nowSM=========${dirList[i]}
	
	./pipe_softRDmultiprocessing.sh ${bamfolder}  ${smfolder}/${dirList[i]} ${outfolder} ${coretouse}

	(( i++ ))

done




suffix=binnedstats.pkl


suffixoutfolderdupNondup=${outfolder}_${suffix}
./run_collectall_statfiles_pickle.sh ${outfolder} ${suffix} ${suffixoutfolderdupNondup}


suffixoutfolder=${suffixoutfolderdupNondup}_onlydup


mkdir ${suffixoutfolder}

cp ${suffixoutfolderdupNondup}/*result_dupindex_binnedstats.pkl ${suffixoutfolder}/


scoreoutfolder=${suffixoutfolder}_softRC
./run_scoreflexible.sh ${suffixoutfolder} ${scoreoutfolder}



cttotalfragmentfolder=${suffixoutfolder}_ctTotalFrag
./run_cellsepcificTotalFragment.sh ${suffixoutfolder} ${cttotalfragmentfolder}




divbyctfragfoler=${scoreoutfolder}_divbyctFrag
./run_mixdividebyTotalCtFragment.sh ${cttotalfragmentfolder} ${scoreoutfolder}  ${divbyctfragfoler}






end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



