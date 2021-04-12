start=$SECONDS

imputedfilebed=$1 #${imputedfile}_onlypos.bed
sortedDMRdirectory=$2
targetednumCpG=$3






interwithDMR=${sortedDMRdirectory}_singleCpG
./bedintersect_folder_wb.sh  ${sortedDMRdirectory} ${imputedfilebed} ${interwithDMR}



finaloutdir=${interwithDMR}_final
mkdir ${finaloutdir}

./run_collectrequirednumCpG.sh ${interwithDMR}  ${targetednumCpG}  ${finaloutdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

