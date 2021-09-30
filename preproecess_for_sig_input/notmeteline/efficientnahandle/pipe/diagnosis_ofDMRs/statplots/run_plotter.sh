start=$SECONDS

infolder=$1
annotfolder=$2
mode="Region" #"habijabi" #"AUC_Region" #"Region"  ####or "allgenes"  or  just any other thing to disable it
deltacol=maxCompartmentwisedelta



dirList=($( ls ${annotfolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	outdir=${infolder}_$( basename ${dirList[i]} )_figs
	mkdir ${outdir}
	python3 driver_plotter.py ${infolder} ${deltacol} ${outdir} ${annotfolder}/${dirList[i]} ${mode}
	(( i++ ))
done
 



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
