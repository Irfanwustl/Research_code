infolder=$1

outdir=${infolder}_out_DMC

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	./metilene -f 3 -c 2 -a g1 -b g2 ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}_DMC.txt
 	(( i++ ))
done