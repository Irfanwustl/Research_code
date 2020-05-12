timestart=$SECONDS




##parm1=sig, parm2=hyper_selected, param3=mixin

sig=$1    #Sig_g20_5_manual_filter1  #### Sig
hyper_selected_file=$2     #Sig_g20_5_manual_filter1_selected

mixin=$3        #all_bg_rolled




sigPos=${sig}Onlyposition
python c2b_onlyposition.py  ${sig}  ${sigPos}

echo "c2b_onlyposition.py done"


outdir=${mixin}_${sigPos}_intersected
mkdir ${outdir}

dirList=($( ls ${mixin}  ))



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	


	bedtools intersect -wa -a ${mixin}/${dirList[i]} -b ${sigPos} -F 1 > ${outdir}/${dirList[i]} 
 	(( i++ ))
done



echo "bedintersect done"

./b2c_full_folder.sh ${outdir} ${outdir}_cyberin

echo "b2c_full_folder.sh done"

./run_scale_folder.sh ${outdir}_cyberin  ${outdir}_cyberin_scaled

echo "run_scale_folder.sh done"



timeend=$SECONDS
duration=$(( timeend - timestart))
echo "stuff took $duration seconds to complete"







############### then we need to run invertto_hypo_mixfolder.sh  on ${outdir}_cyberin_scaled . (hypo or hyper should be decided later)#########################
./invert_file_folder.sh ${hyper_selected_file} ${outdir}_cyberin_scaled  ${outdir}_cyberin_scaled_inverted ${outdir}_cyberin_scaled_inverted_selectedinverted


cp ${sig} ${outdir}_cyberin_scaled_inverted_selectedinverted/


a="$(pwd)"

./run_csx.sh ${a}/${outdir}_cyberin_scaled_inverted_selectedinverted ${sig}






