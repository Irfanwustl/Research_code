
inputbam=$1
readnamefile=$2
outbam=$3


samtools view ${inputbam} > ${inputbam}.sam.txt

grep ${inputbam}.sam.txt -f ${readnamefile}      



