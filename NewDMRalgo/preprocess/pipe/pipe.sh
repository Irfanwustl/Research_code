
rowmeanfile=$1 
phenfile=$2 
outfolder=${rowmeanfile}_compdeltafor



mkdir  ${outfolder}



python3 Compartmentwisedelta.py ${rowmeanfile} ${phenfile} ${outfolder}



dirList=($( ls ${outfolder} ))


outfolderbg=${outfolder}_bg


mkdir ${outfolderbg}


i=0
while (( i < ${#dirList[@]} ))
do
	python3 c2b_header_plain.py ${outfolder}/${dirList[i]} ${outfolderbg}/${dirList[i]} 
 	(( i++ ))
done
