

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_incpgisland_distribution.bed_ge_7.txt -u > all_sequences_cpg_incpgisland_distribution.bed_ge_7_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_incpgisland_distribution.bed_ge_5.txt -u > all_sequences_cpg_incpgisland_distribution.bed_ge_5_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_incpgisland_distribution.bed_ge_3.txt -u > all_sequences_cpg_incpgisland_distribution.bed_ge_3_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_incpgisland_distribution.bed_ge_2.txt -u > all_sequences_cpg_incpgisland_distribution.bed_ge_2_CpGs.txt







bedtools intersect -a all_sequences_cpg.bed -b genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_7.txt -u > genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_7_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_5.txt -u > genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_5_CpGs.txt


bedtools intersect -a all_sequences_cpg.bed -b genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_3.txt -u > genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_3_CpGs.txt


bedtools intersect -a all_sequences_cpg.bed -b genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_2.txt -u > genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed_ge_2_CpGs.txt





bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_distribution.bed_ge_7.txt -u > all_sequences_cpg_distribution.bed_ge_7_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_distribution.bed_ge_5.txt -u > all_sequences_cpg_distribution.bed_ge_5_CpGs.txt


bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_distribution.bed_ge_3.txt -u > all_sequences_cpg_distribution.bed_ge_3_CpGs.txt

bedtools intersect -a all_sequences_cpg.bed -b all_sequences_cpg_distribution.bed_ge_2.txt -u > all_sequences_cpg_distribution.bed_ge_2_CpGs.txt

