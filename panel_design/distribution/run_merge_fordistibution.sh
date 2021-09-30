start=$SECONDS



echo "now all_sequences_cpg_incpgisland.bed"

bedtools merge -c 3 -o count_distinct  -d 170 -i all_sequences_cpg_incpgisland.bed > all_sequences_cpg_incpgisland_distribution.bed



echo "now genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin.bed"

bedtools merge -c 3 -o count_distinct  -d 170 -i genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin.bed > genepromoter_1000_1000_sorted_onlypos_merged_all_cpgwithin_distribution.bed



echo "now all_sequences_cpg.bed"

bedtools merge -c 3 -o count_distinct  -d 170 -i all_sequences_cpg.bed > all_sequences_cpg_distribution.bed



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


