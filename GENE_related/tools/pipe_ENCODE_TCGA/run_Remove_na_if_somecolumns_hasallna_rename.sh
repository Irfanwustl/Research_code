infolder=$1



outdir=${infolder}_na_fixed

dirList=($( ls ${infolder}  ))

outdirnaming=${outdir}_namefixed


mkdir ${outdirnaming}



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 Remove_na_if_somecolumns_hasallna.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]} 
	python3 renameENCOD_TCGA.py ${outdir}/${dirList[i]} ${outdirnaming}/${dirList[i]} 
 	(( i++ ))
done