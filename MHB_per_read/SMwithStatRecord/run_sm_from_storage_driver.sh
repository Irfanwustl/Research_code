



statfile=$1
phenfile=$2

qcut=$3
fcut=$4
minnumfeature=$5
maxnumfeature=$6
gap=$7


outname=${statfile}_${qcut}_${fcut}


python3 sm_from_storage_driver.py ${statfile} ${phenfile} ${outname} ${qcut} ${fcut} ${minnumfeature} ${maxnumfeature} ${gap}






