infolder=$1



outdir=${infolder}_cpginfo

dirList=($( ls ${infolder}  ))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	
	
	python3 softRC_cpginfosaveHARDCODED.py ${infolder}/${dirList[i]}  ${outdir}/${dirList[i]}  

	

  	(( i++ ))
done