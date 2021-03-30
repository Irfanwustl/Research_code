infolder=$1 #folder with raw met out like: /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/PBLtILMEL_input_out_mincpg2_head
qcut=$2 #0.01
diffcut=$3 #0.05

stepaoutdir=${infolder}_q${qcut}_diff${diffcut}


./stepa_run_metthresholdpassed.sh ${infolder} ${qcut} ${diffcut} ${stepaoutdir}


headerdir=${stepaoutdir}_header
./run_addheader.sh ${stepaoutdir}  ${headerdir}


dummydir=${headerdir}_dummycol
./run_adddummy.sh ${headerdir} ${dummydir}


###### sort based on hypo hyper #####
./stepd_run_sortDMR_ondiff.sh ${dummydir}
