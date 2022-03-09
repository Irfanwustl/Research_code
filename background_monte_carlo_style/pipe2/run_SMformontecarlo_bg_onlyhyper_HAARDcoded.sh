infolder=$1

howmanySM=$2

totalcpg=1000
avgdelta=-.98

outdir=${infolder}_RandomSMhypercutoff_final

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	
	python3 SMformontecarlo_bg_onlyhyper_fromunionbgHARDcoded.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  ${howmanySM}  ${totalcpg}  ${avgdelta} 0.5
	python3 SMformontecarlo_bg_onlyhyper_fromunionbgHARDcoded.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  ${howmanySM}  ${totalcpg}  ${avgdelta} 0.7
	python3 SMformontecarlo_bg_onlyhyper_fromunionbgHARDcoded.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  ${howmanySM}  ${totalcpg}  ${avgdelta} 0.9

	

  	(( i++ ))
done