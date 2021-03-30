
reffile=$1
phenfile=$2

outname=${reffile}_imputed

python3 imputer.py ${reffile} ${phenfile} ${outname}










