
sm=$1
fianldir=$2


dirList=($( ls ${fianldir} ))




i=0
while (( i < ${#dirList[@]} ))
do

	python3 poscpgfromfinal_moredata.py ${fianldir}/${dirList[i]} ${sm}

	(( i++ ))


done


