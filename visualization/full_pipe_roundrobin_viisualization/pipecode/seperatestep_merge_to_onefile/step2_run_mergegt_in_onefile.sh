

mergedfolder=$1

suffixonefile=$2

smlist=($( ls ${mergedfolder} ))


i=0
while (( i < ${#smlist[@]} ))
do

	gtmergedlist=($( ls ${mergedfolder}/${smlist[i]} ))
	j=0
	while (( j < ${#gtmergedlist[@]} ))
	do
		python3 mergegt_in_onefile.py ${mergedfolder}/${smlist[i]}/${gtmergedlist[j]} ${mergedfolder}/${smlist[i]}/${gtmergedlist[j]}_${suffixonefile}
		(( j++ ))
	done

	(( i++ ))
done