#bedtools intersect -a all_matrix_T1382 -b 3DMR_pos_sorted_merged  -wa -header > master_mat


#bedtools intersect -a all_sig_bg_all_matrix -b 3DMR_pos_sorted_merged  -wa -header > q.25d.1_cyberSigInput

bedtools intersect -a all_sig_bg_rolled_all_matrix -b 3DMR_pos_sorted_merged  -wa -header > q.25d.1_rolled_cyberSigInput