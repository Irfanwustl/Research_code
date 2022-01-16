
reffile=$1
phenfile=$2
rate=$3
outname=${reffile}_nr${rate}

python3 nahandle.py ${reffile} ${phenfile} ${rate} ${outname}


imputeoutname=${outname}_imputed


python3 imputer.py ${outname} ${phenfile} ${imputeoutname}



python3 row_mean.py hqbijabi ${phenfile} ${imputeoutname}  0  ${imputeoutname}_rowmean


python3 c2b_header.py ${imputeoutname}_rowmean ${imputeoutname}_rowmean_bg



python3 Othermean_ALLctfaster.py ${imputeoutname}_rowmean_bg ${phenfile}












