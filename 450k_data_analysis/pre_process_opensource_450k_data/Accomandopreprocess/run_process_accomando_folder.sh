
the450kfolder=$1    ###### like ours sorted folder (like tcga my preprocessed data) 

outdir=${the450kfolder}_gpos

dirList=($( ls ${the450kfolder}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 process_accomando.py genompos450_nostar.txt ${the450kfolder}/${dirList[i]}  ${outdir}/${dirList[i]}
 	(( i++ ))
done
