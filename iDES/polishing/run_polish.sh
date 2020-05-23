freqdir=$1

bgdbfile=$2

outdir=${freqdir}_${bgdbfile}_ploisheddir


mkdir ${outdir}



perl ides-polishbg.pl -o ${outdir} ${freqdir} ${bgdbfile}





