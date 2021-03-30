bamdir=$1
readnamedir=$2


outdir=$3 #${bamdir}_$( basename ${readnamedir} )

outdirlog=${outdir}_log   #### for my version
mkdir ${outdirlog}   #### for my version


dirList=($( ls ${bamdir} | grep -v '\.bai$'))

mkdir ${outdir}

i=0
while (( i < ${#dirList[@]} ))
do

	echo nowbam=========${dirList[i]} 
	
	namelist=($( ls ${readnamedir} ))
	j=0
	while (( j < ${#namelist[@]} ))
	do
		if [[ "${namelist[j]}" == "${dirList[i]}"* ]]; then
  			echo nownamelist=============${namelist[j]}

  			outname=${dirList[i]}_${namelist[j]}
  			./getthecorressbam.sh ${bamdir}/${dirList[i]}  ${readnamedir}/${namelist[j]}  ${outdir}/${outname}  ${outdirlog}/${outname}      ####for my version
		fi
		

		(( j++ ))
	done



 	(( i++ ))
done



