start=$SECONDS


ref=$1 #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/data/q25d1.txt_inverted
pheno=$2 #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/data/meth_phen_class_irf_only_relevant.txt
suffix=hypo ######this is just a suffix to indicate ref file direction


./run_storagedriver.sh ${ref}   ${pheno}  ${suffix}




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"