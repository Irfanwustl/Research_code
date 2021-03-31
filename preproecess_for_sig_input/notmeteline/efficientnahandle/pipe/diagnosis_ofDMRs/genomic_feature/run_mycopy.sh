infolder=$1


outdir=$2


dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	python3 mypycopy.py ${infolder}/${dirList[i]} ${outdir}
 	(( i++ ))
done