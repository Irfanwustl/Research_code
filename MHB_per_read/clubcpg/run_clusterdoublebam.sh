

#### output in the same bam folder


chrstart=$1
chrend=$2

procnum=$3

bamfile=$4

bamfile2=$5

path=$(dirname ${bamfile})

filename=$(basename ${bamfile})




i=${chrstart}
while (( i <= ${chrend} ))
do
	echo chr===${i}


	clubcpg-cluster -a ${bamfile} -b ${bamfile2} --bins ${path}/CompleteBins.${filename}.chr${i}.filtered.csv   --suffix chr${i}  -n ${procnum}

	(( i++ ))
done
