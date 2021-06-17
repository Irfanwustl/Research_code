start=$SECONDS




infile=$1 #/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/ITGAEandERICH1_cin_nr0.5_imputed_rowmean.txt_compdeltafor_CD8TIL.txt


python3 PLET_multiprocess.py ${infile}



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
