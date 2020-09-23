mhbwithcpg=$1 # it should be the file where both cpg and mhb info is stored

mincutoff=$2
maxcutoff=$3

minnumcpgperblock=$4

programname=$5


outdir=${mhbwithcpg}_using${programname}_minCpG${minnumcpgperblock}_minval${mincutoff}_maxval${maxcutoff}

outdirSorted=${outdir}_sorted




mkdir ${outdir}

mkdir ${outdirSorted}

dirList=($( ls ${mhbwithcpg}  ))


echo programname=========${programname}



i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	python3 ${programname} ${mhbwithcpg}/${dirList[i]} ${outdir}/${dirList[i]} ${mincutoff} ${maxcutoff} ${minnumcpgperblock}

	sort -k 1,1 -k2,2n ${outdir}/${dirList[i]} > ${outdirSorted}/${dirList[i]} 

 	(( i++ ))
done











