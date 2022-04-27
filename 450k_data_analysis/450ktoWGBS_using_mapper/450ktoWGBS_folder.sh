infolder=$1
outdir=${infolder}_WGBS

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 450ktoWGBS.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}_WGBS
 	(( i++ ))
done