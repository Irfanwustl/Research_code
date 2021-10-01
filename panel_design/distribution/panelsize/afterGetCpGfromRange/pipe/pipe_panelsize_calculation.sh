infolder=$1
outdir=${infolder}_panelsize

dirList=($( ls ${infolder}  ))


mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 


	python3 addoffset.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}

	bedtools merge  -i ${outdir}/${dirList[i]} >  ${outdir}/${dirList[i]}_merged

	python3  calculate_panelsize.py ${outdir}/${dirList[i]}_merged ${outdir}/${dirList[i]}_merged_panelsize.txt

	(( i++ ))
	
done