timestart=$SECONDS




##parm1=sig, parm2=hyper_selected, param3=mixin

sig=$1    #Sig_g20_5_manual_filter1  #### Sig
#hyper_selected_file=$2     #Sig_g20_5_manual_filter1_selected

mixin=$2        #all_bg_rolled




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




cp ${sig} ${outdir}_cyberin/


a="$(pwd)"

./run_csx.sh ${a}/${outdir}_cyberin ${sig}






