




the450kpositionsFile=$1  

wgbsFolder=$2  #### rolled


outdir=${wgbsFolder}_${the450kpositionsFile}_convertedto450k


dirList=($( ls ${wgbsFolder}  ))

mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -wa -a ${wgbsFolder}/${dirList[i]} -b ${the450kpositionsFile} -F 1 > ${outdir}/${dirList[i]}_convertedto450k
 	(( i++ ))
done




