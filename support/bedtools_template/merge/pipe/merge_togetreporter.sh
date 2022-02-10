
the450kfolder=$1    ###### like ours sorted folder (like tcga my preprocessed data) 

outdir=${the450kfolder}_mergedtogetreporter

dirList=($( ls ${the450kfolder}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools merge -i ${the450kfolder}/${dirList[i]} -d 150 -c 1 -o count  > ${outdir}/${dirList[i]}
 	(( i++ ))
done

