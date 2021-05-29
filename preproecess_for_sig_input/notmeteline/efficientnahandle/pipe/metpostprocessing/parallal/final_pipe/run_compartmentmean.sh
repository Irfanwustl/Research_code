

imputedfile=$1  #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/promdataready_all_matrixCin_nr0.5_imputed_head.txt 
metoutfolder=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt
qcut=0.5

outname=${imputedfile}_rowmean.txt







python3  row_mean.py ${metoutfolder} ${phenfile} ${imputedfile} 0 ${outname}




./run_compartmentmean_ifrowmean.sh ${outname} ${metoutfolder} ${phenfile} ${qcut}


