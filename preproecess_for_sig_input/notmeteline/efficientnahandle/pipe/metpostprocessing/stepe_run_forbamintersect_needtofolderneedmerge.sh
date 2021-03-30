infolder=$1 #final sorted
forbamnumofDMR=$2
forbamoffset=150

outdir=${infolder}_g${forbamnumofDMR}forbam

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


python3 forbamintersect.py ${infolder} ${forbamnumofDMR}  ${forbamoffset}  ${outdir}

