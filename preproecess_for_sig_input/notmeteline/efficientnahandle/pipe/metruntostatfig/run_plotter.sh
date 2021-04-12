start=$SECONDS

infolder=$1
deltacol=maxCompartmentwisedelta
outdir=${infolder}_${deltacol}_figs





mkdir ${outdir}


 
python3 driver_plotter.py ${infolder} ${deltacol} ${outdir}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
