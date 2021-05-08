start=$SECONDS

imputedfilebed=$1 #${imputedfile}_onlypos.bed
sortedDMRdirectory=$2
targetednumDMR=$3




onlytopdmr=${sortedDMRdirectory}_top${targetednumDMR}
./run_onlytopdmr.sh ${sortedDMRdirectory} ${targetednumDMR} ${onlytopdmr}


interwithDMR=${onlytopdmr}_singleCpG
./bedintersect_folder_wb.sh  ${onlytopdmr} ${imputedfilebed} ${interwithDMR}



finaloutdir=${interwithDMR}_final
mkdir ${finaloutdir}

python3 finalref.py ${interwithDMR} ${finaloutdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

