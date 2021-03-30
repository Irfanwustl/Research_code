infolder=$1
outdir=$2

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo nowheader=========${dirList[i]} 
	python3 addheader.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done