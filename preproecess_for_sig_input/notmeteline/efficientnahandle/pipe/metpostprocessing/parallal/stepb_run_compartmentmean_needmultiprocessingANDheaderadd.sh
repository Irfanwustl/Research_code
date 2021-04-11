start=$SECONDS

imputedfile=$1  #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/promdataready_all_matrixCin_nr0.5_imputed_head.txt 
metoutfolder=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt

outdir=${metoutfolder}_addedcol

mkdir ${outdir}


dirList=($( ls ${metoutfolder}  ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 compartmentmean_parallal.py ${imputedfile}  ${metoutfolder}/${dirList[i]} ${phenfile}  ${outdir}/${dirList[i]}
 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



