start=$SECONDS


rowmeanfile=$1 

rawmetoutfile=$2

phenfile=$3 


outfolder=${rowmeanfile}_compdeltafor


echo "Compartmentwisedelta"

mkdir  ${outfolder}



python3 Compartmentwisedelta.py ${rowmeanfile} ${phenfile} ${outfolder}



echo "c2b_header_plain"

dirList=($( ls ${outfolder} ))


outfolderbg=${outfolder}_bg


mkdir ${outfolderbg}


i=0
while (( i < ${#dirList[@]} ))
do
	python3 c2b_header_plain.py ${outfolder}/${dirList[i]} ${outfolderbg}/${dirList[i]} 
 	(( i++ ))
done



echo "bedwithpy"

bedwithpyout=${rawmetoutfile}_intersected

mkdir ${bedwithpyout}

python3 bedwithpy.py ${outfolderbg} ${rawmetoutfile} ${bedwithpyout}







echo "addheader"

readyforpelt=${bedwithpyout}_readyforPELT

mkdir ${readyforpelt}

bedwithpyoutdirList=($( ls ${bedwithpyout}  ))

i=0
while (( i < ${#bedwithpyoutdirList[@]} ))
do


	python3 addheader.py ${bedwithpyout}/${bedwithpyoutdirList[i]} ${readyforpelt}/${bedwithpyoutdirList[i]} 
 	(( i++ ))
done




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


