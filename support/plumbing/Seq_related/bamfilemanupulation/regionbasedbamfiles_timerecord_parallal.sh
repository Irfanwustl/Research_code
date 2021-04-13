start=$SECONDS

region=$1
inbamfolder=$2

bamoutdir=${inbamfolder}_onlyregionIN_${region}

dirList=($( ls ${inbamfolder} ))

mkdir ${bamoutdir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	samtools view -b -L ${region} -h -o ${bamoutdir}/${dirList[i]}_onlyregionIN_${region}.bam -@ 30 ${inbamfolder}/${dirList[i]}
	(( i++ ))
done




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
