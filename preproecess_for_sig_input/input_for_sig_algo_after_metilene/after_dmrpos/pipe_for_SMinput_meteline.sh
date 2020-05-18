#! /bin/bash

#parm1=Allmatrix_file consist of SM raw data
#parm2=3DMR_pos_sorted_merged

allmat=$1
Dpsm=$2


out="${Dpsm}_CpG"






bedtools intersect -a ${allmat} -b ${Dpsm}  -wa -header > ${out}


sed '/NA/d' ${out} > ${out}_NO_NA



python b2c.py ${out}_NO_NA 1 ${out}_NO_NA_mat_Ciberin


ciberinScaled=${out}_NO_NA_mat_Ciberin_scaled

python scale_cyberin_file.py ${out}_NO_NA_mat_Ciberin ${ciberinScaled}


inverted=${ciberinScaled}_inverted

Rscript invert_file.R ${ciberinScaled} ${inverted}






