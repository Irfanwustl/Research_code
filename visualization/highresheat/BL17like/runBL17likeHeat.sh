start=$SECONDS

echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.6"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.6


echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.5"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.5

echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.4"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.4


echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.3"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.3


echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.2


echo "Now BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1"
python3 BL17likeHeat.py BL17in_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

