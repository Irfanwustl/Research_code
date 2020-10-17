

statfile=/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/data/q25d1.txt_inverted_hypo_stat.txt
phenfile=/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/data/meth_phen_class_irf_only_relevant.txt

qcut=0.01
fcut=2
minnumfeature=15
maxnumfeature=25
gap=5


./run_sm_from_storage_driver.sh ${statfile} ${phenfile} ${qcut} ${fcut} ${minnumfeature} ${maxnumfeature} ${gap}


