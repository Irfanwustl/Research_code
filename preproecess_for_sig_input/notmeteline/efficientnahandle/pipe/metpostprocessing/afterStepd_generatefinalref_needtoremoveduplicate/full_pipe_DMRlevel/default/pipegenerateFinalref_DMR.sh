start=$SECONDS

imputedfile=$1
sortedDMRdirectory=$2
targetednumDMR=$3

imputedfilebed=${imputedfile}_onlypos.bed

python3 C2b_flexible-justpos.py ${imputedfile} ${imputedfilebed}


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

