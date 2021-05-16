start=$SECONDS

imputedfile=$1  # rowmean. 
metoutfolder=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt

outdir=${metoutfolder}_addedcol

mkdir ${outdir}





dirList=($( ls ${metoutfolder} ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 compartmentmean_parallal.py ${imputedfile} ${metoutfolder}/${dirList[i]} ${phenfile} ${outdir}/${dirList[i]}
 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



