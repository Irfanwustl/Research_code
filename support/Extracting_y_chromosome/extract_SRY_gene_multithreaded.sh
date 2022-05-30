start=$SECONDS

cram_in=$1 #bamfiles folder ACTUALLY

coretouse=$2

outdir=${cram_in}_SRY

dirList=($( ls ${cram_in} | grep -v '\.bai$'))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	samtools view -b -o $outdir/${dirList[i]}   -@ ${coretouse} ${cram_in}/${dirList[i]} chrY:2786855-2787682
 	(( i++ ))
done

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
