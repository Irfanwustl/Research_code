start=$SECONDS

infolder=$1
annotfile=$2
deltacol=maxCompartmentwisedelta
outdir=${infolder}_$( basename ${annotfile} )_figs





mkdir ${outdir}


 
python3 driver_plotter.py ${infolder} ${deltacol} ${outdir} ${annotfile}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
