

inputfolder=$1
indexfolder=$2

outdir=${inputfolder}_$( basename ${indexfolder} )

dirList=($( ls ${inputfolder} ))

indexfiles=($( ls ${indexfolder} ))

mkdir ${outdir}


j=0
while (( j < ${#indexfiles[@]} ))
do

	echo index=========${indexfiles[j]} 
	i=0
	while (( i < ${#dirList[@]} ))
	do

		echo now=========${dirList[i]} 
		python3 subset_df_using_another_dfindex.py ${inputfolder}/${dirList[i]} ${indexfolder}/${indexfiles[j]} ${outdir}/${dirList[i]}_sub${indexfiles[j]}
	 	(( i++ ))
	done

	(( j++ ))

done
