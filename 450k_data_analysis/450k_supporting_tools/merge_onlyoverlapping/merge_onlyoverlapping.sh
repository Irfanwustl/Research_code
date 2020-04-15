
the450kfolder=$1    ###### like ours sorted folder (like tcga my preprocessed data) 

outdir=${the450kfolder}_mergedonlyoverlapping

dirList=($( ls ${the450kfolder}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	bedtools merge -i ${the450kfolder}/${dirList[i]} -d -1 -c 4 -o mean > ${outdir}/${dirList[i]}
 	(( i++ ))
done

