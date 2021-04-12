infolder=$1 #folder with raw met out like: /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/PBLtILMEL_input_out_mincpg2_head
qcut=$2 #0.01
diffcut=$3 #0.05
outdir=$4 #${infolder}_q${qcut}_diff${diffcut}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 metthresholdpassed.py ${infolder}/${dirList[i]} ${qcut} ${diffcut} ${outdir}/${dirList[i]}_q${qcut}_diff${diffcut}
 	(( i++ ))
done