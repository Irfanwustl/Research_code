

bg_in=$1  #model_data_name_backup_bg_rolled_cyberin

outdir=$2 ####${bg_in}_scaled

dirList=($( ls ${bg_in}  ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python scale_cyberin_folder.py ${bg_in}/${dirList[i]} ${outdir}
 	(( i++ ))
done