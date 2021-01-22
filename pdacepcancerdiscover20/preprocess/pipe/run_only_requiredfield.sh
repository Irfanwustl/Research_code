infolder=$1 #/Users/irffanalahi/Research/Research_code/gitignorefolder/pdacepcamcanerdiscovery/input

outfolder=${infolder}_reqfield

dirList=($( ls ${infolder} ))


mkdir ${outfolder}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 only_requiredfield.py  ${infolder}/${dirList[i]} ${outfolder}/${dirList[i]}
 	(( i++ ))
done

