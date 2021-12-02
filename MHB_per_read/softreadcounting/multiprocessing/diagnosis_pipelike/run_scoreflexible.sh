


binnedfolder=$1


dirList=($( ls ${binnedfolder} | grep -h '\_dupindex_binnedstats.pkl$' ))




i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 


	python3 score_flexible.py ${binnedfolder}/${dirList[i]} 


	(( i++ ))

done




