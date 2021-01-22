infolder=$1
outdir=${infolder}_colorderchanged

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 changeorderofcol.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done