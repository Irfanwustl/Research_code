start=$SECONDS


python3  PosFragment_hypoCpg_distribution.py mNeu1to.1_mincpg1


python3  PosFragment_hypoCpg_distribution.py mNeu1to.1_mincpg3


python3  PosFragment_hypoCpg_distribution.py mNeu1to.1_mincpg5



python3  PosFragment_hypoCpg_distribution.py  BL14_atleast.2_top-1_singleCpG_final_assignedref_uniq.txt_result_final.txt_folder_mincpg1


python3  PosFragment_hypoCpg_distribution.py  BL14_atleast.2_top-1_singleCpG_final_assignedref_uniq.txt_result_final.txt_folder_mincpg3


python3  PosFragment_hypoCpg_distribution.py  BL14_atleast.2_top-1_singleCpG_final_assignedref_uniq.txt_result_final.txt_folder_mincpg5


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"







