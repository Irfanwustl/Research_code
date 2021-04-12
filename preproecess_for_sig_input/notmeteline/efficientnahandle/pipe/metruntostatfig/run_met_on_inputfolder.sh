infolder=$1
mincpg=$2
outdir=$3 #${infolder}_out_mincpg${mincpg}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	./metilene -m ${mincpg} -c 2 -a g1 -b g2 ${infolder}/${dirList[i]}  > ${outdir}/${dirList[i]}.txt
 	(( i++ ))
done