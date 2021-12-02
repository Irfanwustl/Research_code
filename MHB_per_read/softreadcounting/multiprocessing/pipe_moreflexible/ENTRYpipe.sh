
start=$SECONDS


smfolder=$1 

bamfolder=$2 

coretouse=$3






dirList=($( ls ${smfolder} ))

bambase=$( basename ${bamfolder} )

outfolder=${smfolder}_${bambase}_globalout
mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	echo nowSM=========${dirList[i]} 

	./pipe_softRDmultiprocessing.sh ${bamfolder}  ${smfolder}/${dirList[i]} ${outfolder} ${coretouse}

	(( i++ ))

done




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



