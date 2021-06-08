start=$SECONDS

region=$1
inbamfolder=$2

bamoutdir=${inbamfolder}_onlyregionIN_${region}

dirList=($( ls ${inbamfolder} | grep -v '\.bai$' ))

readnamedir=${bamoutdir}_readname

mkdir ${bamoutdir}

mkdir ${readnamedir}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}

	samtools view -M -L ${region} -@ 30 ${inbamfolder}/${dirList[i]} | cut -f1 > ${readnamedir}/${dirList[i]}_readname.txt

	uniq  ${readnamedir}/${dirList[i]}_readname.txt  > ${readnamedir}/${dirList[i]}_readname_uniq.txt

	samtools view -N ${readnamedir}/${dirList[i]}_readname_uniq.txt -b -h -o ${bamoutdir}/${dirList[i]}_onlyregionIN_${region}.bam -@ 30 ${inbamfolder}/${dirList[i]}
	(( i++ ))
done




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
