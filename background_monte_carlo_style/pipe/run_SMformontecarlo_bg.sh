infolder=$1

howmanySM=$2

totalcpg=1000
avgdelta=-.98

outdir=${infolder}_RandomSM

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 SMformontecarlo_HARDCODED_bg.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  ${howmanySM}  ${totalcpg}  ${avgdelta}
  	(( i++ ))
done