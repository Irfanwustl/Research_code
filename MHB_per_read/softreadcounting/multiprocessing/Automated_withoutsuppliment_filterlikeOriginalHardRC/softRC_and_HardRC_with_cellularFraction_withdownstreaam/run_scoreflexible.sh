


binnedfolder=$1

outfolder=$2

sminfofile=$3

source ${sminfofile}

mkdir ${outfolder}


dirList=($( ls ${binnedfolder} | grep -h '\_dupindex_binnedstats.pkl$' ))




i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 

	#echo ${allhardcodedfile[@]}

	python3 score_flexible_HARDCODED.py ${binnedfolder}/${dirList[i]}   ${outfolder}/${dirList[i]} ${allhardcodedfile[@]}


	(( i++ ))

done




