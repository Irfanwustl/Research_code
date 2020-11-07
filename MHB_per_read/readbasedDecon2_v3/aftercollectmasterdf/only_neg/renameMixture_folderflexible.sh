

combinedResultFolder=$1




dirList=($( ls ${combinedResultFolder} ))



i=0
while (( i < ${#dirList[@]} ))
do
	sed -i'.original' -e 's/bg.*negCount.txt/bg/' ${combinedResultFolder}/${dirList[i]}

	(( i++ ))
done






