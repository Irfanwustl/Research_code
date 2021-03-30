infolder=$1 
outdir=${infolder}_pos

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


python3 combinepos.py ${infolder} ${outdir}

