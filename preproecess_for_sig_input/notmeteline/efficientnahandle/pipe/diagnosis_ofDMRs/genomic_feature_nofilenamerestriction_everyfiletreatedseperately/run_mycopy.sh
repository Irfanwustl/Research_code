infolder=$1


outdir=$2


genomicfolder=$3


dirList=($( ls ${infolder}  ))






i=0
while (( i < ${#dirList[@]} ))
do

	python3 mypycopy.py ${infolder}/${dirList[i]} ${outdir}  ${genomicfolder}
 	(( i++ ))
done