infolder=$1



outdir=${infolder}_nafixed

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 Remove_na_if_somecolumns_hasallna.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]} 
 	(( i++ ))
done