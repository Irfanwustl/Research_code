##all parms are met_out files
##out file= _merged




in1=$1
in2=$2
in3=$3

out1=${in1}_pos
out2=${in2}_pos
out3=${in3}_pos



cut -f -3 $in1 > $out1
cut -f -3 $in2 > $out2
cut -f -3 $in3 > $out3


combined_met_pos=3DMR_pos

cat $out1  $out2 $out3 > ${combined_met_pos}



combined_met_pos_sorted=${combined_met_pos}_sorted

sort -k 1,1 -k2,2n ${combined_met_pos} > ${combined_met_pos_sorted}



ulti_out=${combined_met_pos_sorted}_merged

bedtools merge -i ${combined_met_pos_sorted} > ${ulti_out}

