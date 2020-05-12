

bg_in=$1  #epcam_cfdna_bulk_untouched_rolled

outdir=$2 #${bg_in}_cyberin

dirList=($( ls ${bg_in}  ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python b2c_for_full_folder.py ${bg_in}/${dirList[i]} 0 ${outdir}
 	(( i++ ))
done