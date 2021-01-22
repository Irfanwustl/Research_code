statfile=$1 #bluEP_hypo_stat.txt
phenfile=$2 #pblBLUwithneuEPCAMPHENOCLASS.txt

qcut=0.01
fcut=0



python3 sm_from_storage_driver_inf.py ${statfile} ${phenfile} ${qcut} ${fcut}


