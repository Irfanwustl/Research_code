

infolder=$1

howmany=$2

outdir=${infolder}_rankspace

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 towards_rankspace_faster.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}_CpGdelta_info_faster.txt

	python3 heatmap_from_rankspace.py ${outdir}/${dirList[i]}_CpGdelta_info_faster.txt ${howmany}
 	(( i++ ))
done





