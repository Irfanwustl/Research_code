
#### code, data cant be in the same folder. but output in the same bam folder. 



chrstart=$1
chrend=$2

procnum=$3

bamfile=$4

path=$(dirname ${bamfile})

filename=$(basename ${bamfile})




i=${chrstart}
while (( i <= ${chrend} ))
do
	echo chr===${i}


	clubcpg-coverage -a ${bamfile} -n ${procnum} -chr chr${i}

	cat ${path}/CompleteBins.${filename}.chr${i}.csv | awk -F "," '$2>=10 && $3>=2' > ${path}/CompleteBins.${filename}.chr${i}.filtered.csv
	(( i++ ))
done






