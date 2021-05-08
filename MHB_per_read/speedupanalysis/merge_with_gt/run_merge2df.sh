infolder=$1
mergwith=$2
outdir=${infolder}_mergewith${mergwith}

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 merge2df.py ${infolder}/${dirList[i]}  ${mergwith} ${outdir}/${dirList[i]}
 	(( i++ ))
done