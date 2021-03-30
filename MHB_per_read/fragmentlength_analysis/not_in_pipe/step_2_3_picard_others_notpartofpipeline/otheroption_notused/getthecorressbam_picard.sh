
inputbam=$1
readnamefile=$2
outbam=$3


java -jar picard.jar FilterSamReads  I=${inputbam} O=${outbam} READ_LIST_FILE=${readnamefile} FILTER=includeReadList



