
the450kfolder=$1    ###### manualdata

outdir=${the450kfolder}_nomissing

dirList=($( ls ${the450kfolder}  ))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 deletenapos.py ${the450kfolder}/${dirList[i]}  ${outdir}/${dirList[i]}
 	(( i++ ))
done
