



bg_in=$1  ##ciberin_folder, not bg in

phenfile=$2


dirList=($( ls ${bg_in}  ))




i=0
while (( i < ${#dirList[@]} ))
do

	#echo now=========${dirList[i]} 
	python3 heatwithphenoname_fixed.py ${bg_in}/${dirList[i]}  ${phenfile}
 	(( i++ ))
done




