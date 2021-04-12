start=$SECONDS

imputedfile=$1
sortedDMRdirectory=$2
targetednumCpG=$3

imputedfilebed=${imputedfile}_onlypos.bed

python3 C2b_flexible-justpos.py ${imputedfile} ${imputedfilebed}


interwithDMR=${sortedDMRdirectory}_singleCpG
./bedintersect_folder_wb.sh  ${sortedDMRdirectory} ${imputedfilebed} ${interwithDMR}



finaloutdir=${interwithDMR}_final
mkdir ${finaloutdir}

./run_collectrequirednumCpG.sh ${interwithDMR}  ${targetednumCpG}  ${finaloutdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

