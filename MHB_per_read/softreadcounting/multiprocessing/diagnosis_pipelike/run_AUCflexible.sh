


binnedfolder=$1


dirList=($( ls ${binnedfolder} ))




i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 


	python3 AUC_flexible_pickle_ondupindex.py ${binnedfolder}/${dirList[i]} 


	(( i++ ))

done




