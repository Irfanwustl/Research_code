start=$SECONDS

imputedfile=$1  # rowmean. 
metoutfolder=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt

outdir=${metoutfolder}_addedcol

mkdir ${outdir}





#python3  driver_compartmentmean_parallal.py ${metoutfolder} ${phenfile} ${imputedfile} 1 ${outdir}
python3  driver_compartmentmean_slightparallal.py ${metoutfolder} ${phenfile} ${imputedfile} 1 ${outdir}



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



