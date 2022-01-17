infolder=$1



outfolder=${infolder}_stats

mkdir ${outfolder}

dirList=($( ls ${infolder} ))



i=0
while (( i < ${#dirList[@]} ))
do

	

	python3 hashtable_stats-DMRhashtable.py ${infolder}/${dirList[i]} ${outfolder}/${dirList[i]}

	(( i++ ))

done


