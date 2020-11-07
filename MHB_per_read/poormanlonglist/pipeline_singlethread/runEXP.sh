


refsample=$1
phenoclasses=$2

outdir=${refsample}_SM

mkdir ${outdir}


./run_CS_SM_nofeaturelim.sh ${refsample} ${phenoclasses} ${outdir}

