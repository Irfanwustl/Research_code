stepaoutdir=$1

headerdir=${stepaoutdir}_header
./run_addheader.sh ${stepaoutdir}  ${headerdir}


dummydir=${headerdir}_dummycol
./run_adddummy.sh ${headerdir} ${dummydir}


###### sort based on hypo hyper #####
./stepd_run_sortDMR_ondiff.sh ${dummydir}