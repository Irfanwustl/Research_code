infolder=$1

numofline=$2

outdir=${infolder}_headtail${numofline}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 head_tail.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]} ${numofline}
 	(( i++ ))
done