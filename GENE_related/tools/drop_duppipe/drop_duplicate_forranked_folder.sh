infolder=$1
outdir=${infolder}_nodup

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 drop_duplicate_foranked.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done