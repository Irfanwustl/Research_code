

hyper_selected_file=$1 #Sig_g20_5_manual_filter1_selected  #Sigq25d1_hypo.txt_Sigq25d1_hyper.txt_selected



mixfolderIn=$2   #all_bg_rolled_Sig_g20_5_manual_filter1Onlyposition_intersected_cyberin_scaled



outdir=$3 #${mixfolderIn}_inverted

outdirSelectedInvert=$4

dirList=($( ls ${mixfolderIn}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	Rscript invert_file_folder.R ${mixfolderIn}/${dirList[i]} ${outdir}
 	(( i++ ))
done



echo "now selected....."
./selectedinvert_mixfolder.sh   ${outdir}  ${hyper_selected_file}  ${outdirSelectedInvert}
