infolder=$1 #folder with raw met out like: /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/PBLtILMEL_input_out_mincpg2_head
qcut=$2 #0.01
diffcut=$3 #0.05

stepaoutdir=${infolder}_q${qcut}_diff${diffcut}


./run_metthresholdpassed.sh ${infolder} ${qcut} ${diffcut} ${stepaoutdir}




###### sort based on hypo hyper #####
./run_sortDMR_oncompartmentdelta.sh ${stepaoutdir}
