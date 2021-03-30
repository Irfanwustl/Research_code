#! /bin/bash

#parm1=celltyp1
#parm2=celltype2

set -e  # exit if any exception


infile=$1







cut -f2- ${infile}> ${infile}_needed_column


final_input=${infile}_needed_column_final

Rscript data_trans.R ${infile}_needed_column ${final_input}

echo "NOW PCA........"

Rscript high_res_without_disp_abulmgi_candisc20_blu_moreshape.R ${final_input} 








