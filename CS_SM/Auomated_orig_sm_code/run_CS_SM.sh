refsample=$1
phenoclasses=$2
outdir=$3 

Gmin=$4 #50 lm 22
Gmax=$5 #200 lm22

qvalue=0.01 #0.3 lm 22
filter=False

Rscript functional_CS_SM.R ${refsample} ${phenoclasses} ${outdir} ${qvalue} ${Gmin} ${Gmax} ${filter}

