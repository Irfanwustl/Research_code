start=$SECONDS



smfile=$1  #/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_CD4DMRofBL14atleast.2SM.txt_formatted.txt
finalfolder=$2 #/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/mincpg1_somfinal

celltype=CD4

outdir=${finalfolder}_softRD

dirList=($( ls ${finalfolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}

	python3 testtheidea.py ${smfile} ${finalfolder}/${dirList[i]}  ${outdir}/${dirList[i]} ${celltype}

	(( i++ ))
done





end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


