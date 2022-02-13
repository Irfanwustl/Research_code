
start=$SECONDS

reffile=$1
phenfile=$2
compartmentfile=$3

coretouse=$4


outfolder=${reffile}_allout

mkdir ${outfolder}


python3 tieredhashgeneration.py ${reffile}  ${phenfile} ${compartmentfile} ${outfolder}


./ENTRY_parallel.sh ${outfolder} ${coretouse}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


