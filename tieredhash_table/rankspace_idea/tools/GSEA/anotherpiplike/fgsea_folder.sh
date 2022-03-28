infolder=$1

overfitfile=$2

outdir=${infolder}_gsea

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 

	Rscript fgsea_meth_outfile.R ${infolder}/${dirList[i]} ${overfitfile} ${outdir}/${dirList[i]}

	
 	(( i++ ))
done