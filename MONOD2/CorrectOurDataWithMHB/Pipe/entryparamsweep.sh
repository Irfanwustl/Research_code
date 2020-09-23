indir=$1

i=.1
for i in $(seq 0.05 0.05 0.5)
do
	for j in $(seq 0.5 0.05 0.95)
	do
		echo "now i=====${i} and j====${j}"

		./run_anyoftheTWO.sh ${indir} ${i}  ${j}  3  MeanBasedRule.py 

		./run_anyoftheTWO.sh ${indir} ${i}  ${j}  3  MaxBasedRuleNointermediate.py 
	
 	done
done