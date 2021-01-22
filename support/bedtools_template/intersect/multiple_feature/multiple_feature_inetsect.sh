##it works

allmat=$1
Dpsm=$2


out="${Dpsm}_CpG"






bedtools intersect -a ${allmat} -b ${Dpsm}  -wa -header > ${out}


