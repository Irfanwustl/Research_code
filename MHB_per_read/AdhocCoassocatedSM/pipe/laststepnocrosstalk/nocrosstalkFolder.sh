

pready=$1  #/Users/irffanalahi/Research/weekly/for_10_21_20/WithNeu/generatestatsm/singlethread/downstream/removingcrosstalk/allsm_processed_Ready

outdir=${pready}Nocrosstalk

dirList=($( ls ${pready} ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do
	echo now=========${dirList[i]} 

	awk '$4~/,/ {next} {print}' ${pready}/${dirList[i]} > ${outdir}/${dirList[i]}nc.txt

	(( i++ ))
done


