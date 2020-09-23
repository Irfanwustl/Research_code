
all_mat=$1 #blleukog50_hypo.txt

all_mat_bg=${all_mat}_bg
python c2b_onlyposition.py ${all_mat}  ${all_mat_bg}


intersected=${all_mat_bg}_intersecetedwithMHB

bedtools intersect  -a ${all_mat_bg} -b /Users/irffanalahi/Research/Research_code/MONOD2/UseTheirMHB/mond2_mhb_hg38_sorted_merged.bed -wa  -wb > ${intersected}



