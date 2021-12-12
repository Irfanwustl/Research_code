
reffile=$1
phenfile=$2
rate=$3
outname=${reffile}_nr${rate}

python3 nahandle.py ${reffile} ${phenfile} ${rate} ${outname}


imputeoutname=${outname}_imputed


python3 imputer.py ${outname} ${phenfile} ${imputeoutname}














