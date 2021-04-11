infolder=$1
word=$2
outdir=${infolder}_${word}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	grep -i ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}
 	(( i++ ))
done