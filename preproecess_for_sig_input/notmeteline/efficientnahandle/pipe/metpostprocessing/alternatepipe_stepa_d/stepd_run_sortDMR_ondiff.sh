infolder=$1 # /Users/irffanalahi/Research/Research_code/gitignorefolder/SMwithlog_test/metpostprocessing/afteraddcolum/datain_compartmentdiff-0.1
metricindex=4 #3=q,4=diff etc. But here 4 is hardcoded for later.
outdir=${infolder}_sorted${metricindex}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo nowsort=========${dirList[i]} 
	if [[ "${dirList[i]}" == *"hypo"* ]]; then
		
		sortcriteria=1 #1=asc, 2=dsc
  		python3 sortDMR.py ${infolder}/${dirList[i]} ${metricindex} ${sortcriteria}  ${outdir}/${dirList[i]}_${metricindex}_${sortcriteria}.txt
  	else
 
		sortcriteria=2 #1=asc, 2=dsc
  		python3 sortDMR.py ${infolder}/${dirList[i]} ${metricindex} ${sortcriteria}  ${outdir}/${dirList[i]}_${metricindex}_${sortcriteria}.txt
	fi
	
 	(( i++ ))
done