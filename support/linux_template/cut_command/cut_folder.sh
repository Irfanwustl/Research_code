infolder=$1
outdir=${infolder}_cut1_4

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	cut -f 1,4 ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}
 	(( i++ ))
done