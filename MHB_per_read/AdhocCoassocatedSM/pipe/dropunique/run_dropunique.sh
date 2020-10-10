

fileqithblockinfo=$1

startcpgCount=$2

endcpgCount=$3

i=${startcpgCount}

while (( i <= ${endcpgCount} ))
do

	python3 dropunique.py ${fileqithblockinfo}  ${i}
	(( i++ ))
done





