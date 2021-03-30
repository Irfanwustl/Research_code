infile=$1
outfile=$2
proportion=$3   # 20 like 20% 


echo 0.${proportion}


samtools view -@ 20 -b -s 0.${proportion} ${infile} > ${outfile}

