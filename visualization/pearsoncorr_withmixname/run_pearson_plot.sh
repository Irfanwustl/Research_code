

infolder=$1

xaxis=$2
yaxis=$3

outdir=${infolder}_pearson

dirList=($( ls ${infolder} ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	Rscript pearson_plot.R ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}  ${xaxis} ${yaxis}
	
 	(( i++ ))
done