
reffile=$1
phenfile=$2
direction=$3



outfile=${reffile}_${direction}_stat.txt


python3 storagedriver.py ${reffile} ${phenfile}  ${outfile}

