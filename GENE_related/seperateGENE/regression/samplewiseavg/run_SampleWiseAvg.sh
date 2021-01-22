pergeneciberinfolder=$1

outfolder=${pergeneciberinfolder}_forregression

mkdir ${outfolder}


dirList=($( ls ${pergeneciberinfolder} ))





i=0
while (( i < ${#dirList[@]} ))
do
	python3 SampleWiseAvg.py ${pergeneciberinfolder}/${dirList[i]} ${outfolder}/${dirList[i]}
	(( i++ ))
done



 




