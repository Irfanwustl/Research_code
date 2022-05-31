start=$SECONDS


file_directory=$1



geneinfofile=$2


outdir="${file_directory}_pp"


mkdir  ${outdir}
fList=($( ls ${file_directory} ))

i=0
while (( i < ${#fList[@]} ))
#while (( i < 1 ))
do
	echo now=========${fList[i]} 
	samtools view  -b -h -f 0x02 -F 0x100 -@ 8 ${file_directory}/${fList[i]} > ${outdir}/${fList[i]}

	(( i++ ))
done









flag_outdir="${file_directory}_pp_flag"

mkdir ${flag_outdir}

f3List=($( ls ${outdir} ))

i=0

while (( i < ${#f3List[@]} ))
do

	echo flag=========${f3List[i]} 
	samtools flagstat ${outdir}/${f3List[i]} >    ${flag_outdir}/${f3List[i]}_flag

	(( i++ ))
done

./makedepth_mapq_necessary.sh ${outdir} 


python3 Extract_and_depth_all_genes.py  ${outdir}_depthfullinfo ${geneinfofile}





end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"






