
start=$SECONDS


smfolder=$1 

bamfolder=$2 

coretouse=$3

sminfofile=$4

gtfolder=gt

source ${sminfofile}



dirList=($( find ${smfolder} -maxdepth 1 -type f -not -path '*/\.*'))

bambase=$( basename ${bamfolder} )

outfolder=${smfolder}_${bambase}_globalout
mkdir ${outfolder}

allresulttogether=${outfolder}_allSoftRCresultogether   #####except divide by ctfrag. And hard RC to soft RC now is adjusted score. Need to fix this
mkdir ${allresulttogether}




#######this loop should be parallel#######
#i=0
#while (( i < ${#dirList[@]} ))
#do

	
	#echo nowSM=========${dirList[i]}
	
#	./pipe_softRDmultiprocessing.sh ${bamfolder}  ${smfolder}/${dirList[i]} ${outfolder} ${coretouse}

#	(( i++ ))

#done

parallel -j ${coretouse} ./pipe_softRDmultiprocessing.sh ::: ${bamfolder} ::: ${dirList[@]} ::: ${outfolder} ::: ${coretouse}



suffix=binnedstats.pkl


suffixoutfolderdupNondup=${outfolder}_${suffix}
./run_collectall_statfiles_pickle.sh ${outfolder} ${suffix} ${suffixoutfolderdupNondup}


suffixoutfolder=${suffixoutfolderdupNondup}_onlydup


mkdir ${suffixoutfolder}

cp ${suffixoutfolderdupNondup}/*result_dupindex_binnedstats.pkl ${suffixoutfolder}/




scoreoutfolder=${suffixoutfolder}_softRC

#######this script should be parallel####### DONE
./run_scoreflexible.sh ${suffixoutfolder} ${scoreoutfolder} ${sminfofile}

cp ${scoreoutfolder}/*_maxscore_CSxOut.txt ${allresulttogether}/



cttotalfragmentfolder=${suffixoutfolder}_ctTotalFrag
#######this script should be parallel####### DONE
./run_cellsepcificTotalFragment.sh ${suffixoutfolder} ${cttotalfragmentfolder} ${sminfofile}




divbyctfragfoler=${scoreoutfolder}_divbyctFrag
#######this script should be parallel####### DONE
./run_mixdividebyTotalCtFragment.sh ${cttotalfragmentfolder} ${scoreoutfolder}  ${divbyctfragfoler}


#cp ${divbyctfragfoler}/*_maxscore_CSxOut.txt ${allresulttogether}/

echo NowHARDrc

HardRCoudtir=${suffixoutfolder}_HardRC


#######this script should be parallel####### DONE
./run_HardRC.sh ${suffixoutfolder} ${HardRCoudtir} ${sminfofile}
cp ${HardRCoudtir}/*_CSxOut.txt ${allresulttogether}/


echo NowHARDrcTOsoftRC
HARDrcTOsoftRCfolder=${suffixoutfolder}_HardRCtoSoftRC


#######this script should be parallel####### DONE
./run_HardRCtosoftRC.sh ${suffixoutfolder} ${HARDrcTOsoftRCfolder} ${sminfofile}

cp ${HARDrcTOsoftRCfolder}/*_CSxOut.txt ${allresulttogether}/



echo NowMaxscoreBasedFraction

finalbinnedfolder=${HARDrcTOsoftRCfolder}_FINALbinned
mkdir  ${finalbinnedfolder}

cp ${HARDrcTOsoftRCfolder}/*FINAL_binnedstats.pkl ${finalbinnedfolder}/

maxscoreFtaction=${scoreoutfolder}_maxscoreFraction

#######this script should be parallel####### DONE 
./run_softRC_theoritical.sh ${finalbinnedfolder} ${scoreoutfolder} ${smfolder} ${maxscoreFtaction} ${sminfofile}
cp ${maxscoreFtaction}/*_maxscore_CSxOut.txt ${allresulttogether}/




echo Now method1 fraction
method1fraction=${scoreoutfolder}_method1Fraction

#######this script should be parallel#######
./run_ct_proportion_idea1.sh ${scoreoutfolder} ${smfolder} ${method1fraction}
cp ${method1fraction}/*_maxscore_CSxOut.txt ${allresulttogether}/


./renameMixture_folderflexible.sh ${allresulttogether}
./renameMixture_folderflexible2.sh ${allresulttogether}
./renameMixture_folderflexible3.sh ${allresulttogether}

rm ${allresulttogether}/*original




echo Now downstream
 
mergedwithGroundTruth=${allresulttogether}_mereged_${gtfolder}

./downstream.sh ${allresulttogether} ${gtfolder} ${mergedwithGroundTruth} ${coretouse}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



