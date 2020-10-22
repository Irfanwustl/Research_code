

combinedResultFolder=$1




dirList=($( ls ${combinedResultFolder} ))



i=0
while (( i < ${#dirList[@]} ))
do
	sed -i'.original' -e 's/bg_howsm_single_mode_pp_ABSreadcount_divisioned.txt/bg/' ${combinedResultFolder}/${dirList[i]}

	(( i++ ))
done






