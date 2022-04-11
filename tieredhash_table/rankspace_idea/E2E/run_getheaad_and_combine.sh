infolder=$1  

topnumber=$2
outdir=${infolder}_top${topnumber}




dirList=($( ls ${infolder} ))

mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	
	python3 gethead.py ${infolder}/${dirList[i]} ${outdir}/${dirList[i]} ${topnumber}
	
 	(( i++ ))
done



python3 mergealldfinafolderrbindlike.py ${outdir} ${outdir}_SM


python3 remove_duplicate.py ${outdir}_SM
