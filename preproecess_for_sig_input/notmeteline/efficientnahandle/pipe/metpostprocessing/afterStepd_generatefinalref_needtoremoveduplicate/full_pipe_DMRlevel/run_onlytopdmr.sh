infolder=$1
targetdmr=$2
outdir=$3

mkdir ${outdir}

dirList=($( ls ${infolder}  ))

i=0
while (( i < ${#dirList[@]} ))
do

	echo nowtopDMR=========${dirList[i]} 
	python3 onlytopdmr.py ${infolder}/${dirList[i]} ${targetdmr} ${outdir}/${dirList[i]} 
 	(( i++ ))
done