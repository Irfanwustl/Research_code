infolder=$1



outdir=${infolder}_avg_background

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	
	python3 avg_background.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  
	
	

  	(( i++ ))
done