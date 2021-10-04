
infolder=$1
intwith=$2

intwithbase=$( basename ${intwith} )

outdir=$3 #${infolder}_intersectedwith_${intwithbase}


dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	head -n 1 ${infolder}/${dirList[i]} > ${outdir}/${dirList[i]}_header_tmp.txt
	head -n 1 ${intwith} > ${outdir}/${intwithbase}_header_tmp.txt

	paste ${outdir}/${dirList[i]}_header_tmp.txt ${outdir}/${intwithbase}_header_tmp.txt > ${outdir}/${dirList[i]}_${intwithbase}_header_tmp.txt

	tail -n +2 ${infolder}/${dirList[i]} > ${outdir}/${dirList[i]}_tail_tmp.txt
	tail -n +2 ${intwith} > ${outdir}/${intwithbase}_tail_tmp.txt 

	bedtools intersect -wa -wb -a ${outdir}/${dirList[i]}_tail_tmp.txt -b ${outdir}/${intwithbase}_tail_tmp.txt  > ${outdir}/${dirList[i]}_${intwithbase}_tail_tmp.txt

	cat  ${outdir}/${dirList[i]}_${intwithbase}_header_tmp.txt ${outdir}/${dirList[i]}_${intwithbase}_tail_tmp.txt > ${outdir}/${dirList[i]}_${intwithbase}.txt

	

	rm ${outdir}/*tmp.txt

 	(( i++ ))
done



