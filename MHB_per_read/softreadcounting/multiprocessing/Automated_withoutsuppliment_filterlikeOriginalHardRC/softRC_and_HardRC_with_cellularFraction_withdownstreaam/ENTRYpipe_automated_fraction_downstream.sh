
start=$SECONDS


smfolder=$1 

bamfolder=$2 

coretouse=$3

gtfolder=gt




dirList=($( ls ${smfolder} ))

bambase=$( basename ${bamfolder} )

outfolder=${smfolder}_${bambase}_globalout
mkdir ${outfolder}

allresulttogether=${outfolder}_allSoftRCresultogether   #####except hard  RC and Soft RC mincpg cutoff and divide by ctfrag
mkdir ${allresulttogether}



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

cp ${scoreoutfolder}/*_maxscore_CSxOut.txt ${allresulttogether}/



cttotalfragmentfolder=${suffixoutfolder}_ctTotalFrag
./run_cellsepcificTotalFragment.sh ${suffixoutfolder} ${cttotalfragmentfolder}




divbyctfragfoler=${scoreoutfolder}_divbyctFrag
./run_mixdividebyTotalCtFragment.sh ${cttotalfragmentfolder} ${scoreoutfolder}  ${divbyctfragfoler}


#cp ${divbyctfragfoler}/*_maxscore_CSxOut.txt ${allresulttogether}/

echo NowHARDrc

./run_HardRC.sh ${suffixoutfolder}

echo NowHARDrcTOsoftRC
HARDrcTOsoftRCfolder=${suffixoutfolder}_HardRCtoSoftRC
./run_HardRCtosoftRC.sh ${suffixoutfolder} ${HARDrcTOsoftRCfolder}

#cp ${HARDrcTOsoftRCfolder}/*_maxscore_CSxOut.txt ${allresulttogether}/



echo NowMaxscoreBasedFraction

finalbinnedfolder=${HARDrcTOsoftRCfolder}_FINALbinned
mkdir  ${finalbinnedfolder}

cp ${HARDrcTOsoftRCfolder}/*FINAL_binnedstats.pkl ${finalbinnedfolder}/

maxscoreFtaction=${scoreoutfolder}_maxscoreFraction

./run_softRC_theoritical.sh ${finalbinnedfolder} ${scoreoutfolder} ${smfolder} ${maxscoreFtaction}
cp ${maxscoreFtaction}/*_maxscore_CSxOut.txt ${allresulttogether}/




echo Now method1 fraction
method1fraction=${scoreoutfolder}_method1Fraction
./run_ct_proportion_idea1.sh ${scoreoutfolder} ${smfolder} ${method1fraction}
cp ${method1fraction}/*_maxscore_CSxOut.txt ${allresulttogether}/


./renameMixture_folderflexible.sh ${allresulttogether}
./renameMixture_folderflexible2.sh ${allresulttogether}
./renameMixture_folderflexible3.sh ${allresulttogether}

rm ${allresulttogether}/*original




echo Now downstream
 
mergedwithGroundTruth=${allresulttogether}_mereged_${gtfolder}

./downstream.sh ${allresulttogether} ${gtfolder} ${mergedwithGroundTruth}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



