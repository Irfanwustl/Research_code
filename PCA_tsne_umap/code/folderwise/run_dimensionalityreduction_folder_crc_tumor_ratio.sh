

infolder=$1 


outdir=${infolder}_PCA




dirList=($( ls ${infolder} ))

mkdir ${outdir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}

	python3  dimensionalityreduction_folder_crc_tumor_ratio.py ${infolder}/${dirList[i]}  ${outdir}

	(( i++ ))
done



