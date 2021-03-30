infolder=$1

outdir=${infolder}_lenrefCPG



dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 cal_lenofrefcpg.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))

done
