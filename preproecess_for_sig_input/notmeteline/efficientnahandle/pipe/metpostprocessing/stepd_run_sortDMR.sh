infolder=$1 # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/afteraddcolum/datain_compartmentdiff-0.1
metricindex=$2 #3=q,4=diff etc.
sortcriteria=$3 #1=asc, 2=dsc
outdir=${infolder}_sorted${metricindex}_${sortcriteria}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 sortDMR.py ${infolder}/${dirList[i]} ${metricindex} ${sortcriteria}  ${outdir}/${dirList[i]}_${metricindex}_${sortcriteria}.txt
 	(( i++ ))
done