infolder=$1


outdir=$2


dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	python3 addheader_withgenomicfeatture.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done