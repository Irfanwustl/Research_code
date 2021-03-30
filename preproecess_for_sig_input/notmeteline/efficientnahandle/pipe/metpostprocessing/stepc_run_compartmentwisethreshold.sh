infolder=$1 #folder with addedcol like /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/afteraddcolum/datain
diffcut=$2 #0.05 or -0.05
outdir=${infolder}_compartmentdiff${diffcut}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 compartmentwisethreshold.py ${infolder}/${dirList[i]} ${diffcut} ${outdir}/${dirList[i]}_compartmentdiff${diffcut}.txt
 	(( i++ ))
done