infolder=$1

x=2
y=26

outdir=${infolder}_out_DMC_X${x}_Y${y}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	./metilene -f 3 -c 2  -X ${x} -Y ${y}   -a g1 -b g2 ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}_DMC.txt
 	(( i++ ))
done