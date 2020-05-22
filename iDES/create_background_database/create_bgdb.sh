

freqdir=$1

mindepth=$2

outdir=${freqdir}_depth${mindepth}_bgdbdir

outfile=${freqdir}_depth${mindepth}_bgdb.txt


perl ides-makedb.pl -o ${outdir} -d ${mindepth} -a ${outfile} ${freqdir}

