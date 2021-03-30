infolder=$1

outdir=${infolder}_dropdup



dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 drop_dup.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}_uniq.txt
 	(( i++ ))

done
