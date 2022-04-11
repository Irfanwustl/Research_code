
start=$SECONDS

reffile=$1
phenfile=$2
compartmentfile=$3

coretouse=$4

MAXWORKER=$5

howmany=$6


outfolder=${reffile}_allout

mkdir ${outfolder}


python3 tieredhashgeneration.py ${reffile}  ${phenfile} ${compartmentfile} ${outfolder}  ${MAXWORKER}

echo now rankspace

./Entry_rankspace.sh ${outfolder} ${howmany} ${reffile} ${compartmentfile}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


