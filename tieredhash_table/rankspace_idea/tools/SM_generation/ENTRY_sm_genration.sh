#SM generate from rankfile
######
#1. convert to SM
#2. take top n number
#3. combine equal number of different cell types

start=$SECONDS


infolder=$1  #/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/rankspace_idea/ALLct/SM/SMin

outdir=${infolder}_SM


dirList=($( ls ${infolder} ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 sm_from_rankinfoHARDCODED.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]}
	
 	(( i++ ))
done


./run_getheaad_and_combine.sh ${outdir} 50

./run_getheaad_and_combine.sh ${outdir} 100

./run_getheaad_and_combine.sh ${outdir} 500


./run_getheaad_and_combine.sh ${outdir} 1000

./run_getheaad_and_combine.sh ${outdir} 1500



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



