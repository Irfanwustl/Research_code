start=$SECONDS

imputedfile=$1  #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/promdataready_all_matrixCin_nr0.5_imputed_head.txt 
metoutfolder=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt

outdir=$4 #${metoutfolder}_addedcol

mkdir ${outdir}





python3  driver_compartmentmean_parallal.py ${metoutfolder} ${phenfile} ${imputedfile} 0 ${outdir}



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



