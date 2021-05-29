start=$SECONDS

imputedfilecin=$1  # rowmean_cin
metoutfolderraw=$2  # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/PBLtILMEL_input_out_mincpg2_head
phenfile=$3      #/Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/add_column/pbltilMELtumor_abulmelMGI_PHENOCLASS.txt
qcut=$4 ####0.05


imputedfile=${imputedfilecin}_bg

python3 c2b_header.py ${imputedfilecin} ${imputedfile}



metoutfolder=${metoutfolderraw}_q${qcut}
./run_qcut.sh ${metoutfolderraw} ${qcut} ${metoutfolder}




outdir=${metoutfolder}_addedcol

imputedfilebgdirectory=${imputedfile}_intersectedbg

mkdir ${imputedfilebgdirectory}

mkdir ${outdir}





dirList=($( ls ${metoutfolder} ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools intersect -wa -wb -a ${imputedfile} -b ${metoutfolder}/${dirList[i]}  -header > ${imputedfilebgdirectory}/${dirList[i]}_bg

	python b2c.py ${imputedfilebgdirectory}/${dirList[i]}_bg 1 ${imputedfilebgdirectory}/${dirList[i]}_bg_cin.txt


	echo now=========compartmentmean
	python3 compartmentmean.py ${imputedfilebgdirectory}/${dirList[i]}_bg_cin.txt ${phenfile} ${outdir}/${dirList[i]}

 	(( i++ ))
done



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



