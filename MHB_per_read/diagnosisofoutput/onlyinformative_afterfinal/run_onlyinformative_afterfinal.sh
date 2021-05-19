infolder=$1 #masterdf or finaldf.like: /Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/readbaseddecon3/postanalysis/forheatmap/datain
outdir=${infolder}_informative

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 onlyinformative_afterfinal.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
 	(( i++ ))
done