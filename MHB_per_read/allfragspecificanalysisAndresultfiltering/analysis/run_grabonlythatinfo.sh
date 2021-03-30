infolder=$1
infocolname=$2
outfolder=$3

mkdir ${outfolder}

dirList=($( ls ${infolder}  ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 grabonlythatinfo.py ${infolder}/${dirList[i]} ${infocolname} ${outfolder}/${dirList[i]}_${infocolname}.txt
 	(( i++ ))
done