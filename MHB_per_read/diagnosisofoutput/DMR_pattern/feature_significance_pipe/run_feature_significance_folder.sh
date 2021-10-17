start=$SECONDS

python3 feature_significance_folder.py BL14_atleast.2_top-1_singleCpG_final_assignedref_uniq.txt_result_final.txt_folder_mincpg1 BL14_atleast.2_top-1_singleCpG_final_record.txt


python3 feature_significance_folder.py mNeu1to.1_mincpg1 BL14_atleast.2_top-1_singleCpG_final_record.txt


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


