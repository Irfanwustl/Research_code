
the450kfolder=$1    ###### like ours sorted folder (like tcga my preprocessed data) 

outdir=${the450kfolder}_uniq

dirList=($( ls ${the450kfolder}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	sort -k1,1 -k2,2n -k3,3n -u ${the450kfolder}/${dirList[i]} > ${outdir}/${dirList[i]}
 	(( i++ ))
done

