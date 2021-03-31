infolder=$1





dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	python3 mergealldfinafolderrbindlike.py ${infolder}/${dirList[i]}
 	(( i++ ))
done