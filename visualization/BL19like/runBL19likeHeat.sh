start=$SECONDS

echo "Now BL19v2metin_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.6"
python3 BL19likeHeat.py /Users/irffanalahi/Research/Research_update/SM/ShowcaseSM/BL19_V2/forfig/myversion/BL19v2metin_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.6





python3 BL19likeHeat.py /Users/irffanalahi/Research/Research_update/SM/ShowcaseSM/BL19_V2/forfig/myversion/BL19v2metin_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1_rarect



python3 BL19likeHeat.py /Users/irffanalahi/Research/Research_update/SM/ShowcaseSM/BL19_V2/forfig/myversion/BL19v2metin_out_mincpg2_q0.5_addedcol_q1e-05_maxCompartmentwisedelta-0.1_rarect_goodothers



end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"

