
fileqithblockinfoFolder=$1


startcpgCount=$2

endcpgCount=$3

outdir=${fileqithblockinfoFolder}_Ready

mkdir ${outdir}

dirList=($( ls ${fileqithblockinfoFolder} ))


i=0
while (( i < ${#dirList[@]} ))
do
	./run_dropunique.sh  ${fileqithblockinfoFolder}/${dirList[i]}  ${startcpgCount} ${endcpgCount} ${outdir}

	(( i++ ))
done



