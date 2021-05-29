infolder=$1 #folder with raw met out like: /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/PBLtILMEL_input_out_mincpg2_head
qcut=$2 #0.01

outdir=${3}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 qcutoff.py ${infolder}/${dirList[i]} ${qcut} ${outdir}/${dirList[i]}
 	(( i++ ))
done