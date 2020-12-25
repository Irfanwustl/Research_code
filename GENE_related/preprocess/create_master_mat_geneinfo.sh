
dmrpos=$1 #genefile #mdiff5_sorted_merged  #all_combined_sorted_merged

allmat=$2


bedtools intersect  -a ${allmat} -b ${dmrpos}  -wa -header -wb > ${allmat}_intesectedwith_${dmrpos}


