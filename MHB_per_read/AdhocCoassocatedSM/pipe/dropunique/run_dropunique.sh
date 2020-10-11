

fileqithblockinfo=$1

startcpgCount=$2

endcpgCount=$3


outdir=$4

i=${startcpgCount}

while (( i <= ${endcpgCount} ))
do

	fname=$( basename ${fileqithblockinfo} )

	python3 dropunique.py ${fileqithblockinfo}  ${i} ${outdir}/${fname}_${i}cpg
	(( i++ ))
done





