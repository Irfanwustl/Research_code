infolder=$1

outfolder=${infolder}_subsetoffinal

mkdir ${outfolder}

dirList=($( ls ${infolder}  ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 grabmultipleinfo.py ${infolder}/${dirList[i]} ${outfolder}/${dirList[i]}
 	(( i++ ))
done