infolder=$1
outdir=${infolder}_majorlineage

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 BL22tomajorlineage.py ${infolder}/${dirList[i]}   ${outdir}/${dirList[i]}
 	(( i++ ))
done