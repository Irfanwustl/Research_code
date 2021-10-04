infolder=$1
outdir=${infolder}_moneyRegion

dirList=($( ls ${infolder}  ))


mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 moneyRegion.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}.pdf
 	(( i++ ))
done


