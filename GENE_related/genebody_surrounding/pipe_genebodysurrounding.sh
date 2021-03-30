ucscfile=$1  # /Users/irffanalahi/Research/Research_code/gitignorefolder/gene/promoter_generator/All_Gene_Info_head.txt


upstream=$2

downstream=$3

outname=${ucscfile}_gebebody${upstream}_${downstream}.txt


python3 genebodysurrounding.py ${ucscfile} ${upstream} ${downstream}  ${outname}


sort -k 1,1 -k2,2n ${outname} > ${outname}_sorted

bedtools merge -d -1 -i ${outname}_sorted > ${outname}_sorted_merged.txt

