start=$SECONDS

imputedfile=$1   #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/towards_final_ref/againtest/numberofDMR/flexiblecolumn/promdataready_all_matrixCin_nr0.5_imputed_head20.txt
sortedDMRdirectory=$2 #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/towards_final_ref/againtest/numberofDMR/flexiblecolumn/PBLtILMEL_input_out_mincpg2_head_addedcol_sorted3_1
targetednumDMR=$3  #5 negative means all dmr

imputedfilebed=${imputedfile}_onlypos.bed

python3 C2b_flexible-justpos.py ${imputedfile} ${imputedfilebed}


onlytopdmr=${sortedDMRdirectory}_top${targetednumDMR}
./run_onlytopdmr.sh ${sortedDMRdirectory} ${targetednumDMR} ${onlytopdmr}


interwithDMR=${onlytopdmr}_singleCpG
./bedintersect_folder_wb.sh  ${onlytopdmr} ${imputedfilebed} ${interwithDMR}



finaloutdir=${interwithDMR}_final
mkdir ${finaloutdir}

python3 finalref.py ${interwithDMR} ${finaloutdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

