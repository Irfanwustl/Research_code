mixfolderIn=$1      #model_data_name_backup_bg_rolled_cyberin_scaled

hyper_selected_file=$2           #Sigq25d1_hypo.txt_Sigq25d1_hyper.txt_selected

outdir=$3   #${mixfolderIn}_selectedinverted

dirList=($( ls ${mixfolderIn}  ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python selectedinvert_mix_corrected.py ${mixfolderIn}/${dirList[i]} ${hyper_selected_file} ${outdir}
 	(( i++ ))
done