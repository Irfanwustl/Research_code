ucscfile=$1  # /Users/irffanalahi/Research/Research_code/gitignorefolder/gene/promoter_generator/All_Gene_Info_head.txt


upstream=1000

outname=${ucscfile}_prom${upstream}


python3 generate_promoter.py ${ucscfile} ${upstream}  ${outname}


sort -k 1,1 -k2,2n ${outname} > ${outname}_sorted

