





bamfolder=$1
smfile=$2

globalout=$3

coretouse=$4

smbasename=$( basename ${smfile} )




outdir=${globalout}/${smbasename}_result

dirList=($( ls ${bamfolder} | grep -v '\.bai$'))



mkdir ${outdir}


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]}
	

	python3 softRDmultiprocessing.py ${bamfolder}/${dirList[i]} ${smfile}  ${outdir}/${dirList[i]} ${coretouse}

	(( i++ ))
done



python3 combineresult_formergingwithgt.py ${outdir}






