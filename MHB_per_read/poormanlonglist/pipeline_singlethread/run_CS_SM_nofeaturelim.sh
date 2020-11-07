

refsample=$1
phenoclasses=$2
outdir=$3



qvalue=0.01

FC=0




python3 driver_sm_generator_nofeaturelim.py ${refsample} ${phenoclasses} ${outdir} ${qvalue} ${FC} 
