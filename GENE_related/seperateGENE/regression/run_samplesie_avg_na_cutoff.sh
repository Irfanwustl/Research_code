pergeneciberinfolder=$1

outfolder=${pergeneciberinfolder}_NAhandled_forregression

mkdir ${outfolder}


dirList=($( ls ${pergeneciberinfolder} ))





i=0
while (( i < ${#dirList[@]} ))
do
	python3 samplesie_avg_na_cutoff.py ${pergeneciberinfolder}/${dirList[i]} ${outfolder}/${dirList[i]}
	(( i++ ))
done



 




